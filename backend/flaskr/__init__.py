import os
from select import select
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# function to paginate the questions
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

     # Set up CORS. Allow '*' for origins.
    CORS(app)

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Endpoint to handle GET requests
    # for all available categories.
    @app.route('/categories', methods=['GET'])
    def get_categories():
        selection = Category.query.order_by(Category.id).all()
        current_categories = paginate_questions(request, selection)
        
        if len(current_categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in selection}
        })

    # Endpoint to handle GET request to get all the questions and the categories
    @app.route('/questions')
    def get_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            
            if len(current_questions) == 0:
                abort(404)

            #get all the questions categories
            categories = Category.query.all()
            categories_dict = {}
            for category in categories:
                categories_dict[category.id] = category.type

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(Question.query.all()),
                'categories': categories_dict
            })
        except:
            abort(404)

    # Endpoint to DELETE question using a question ID.
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            # check if the question exists
            if question is None:
                abort(404)
            
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'question': current_questions,
                'total_questions': len(Question.query.all())
            })
        
        except:
            abort(422)

    # endpoint to POST a new question
    @app.route('/questions', methods=['POST'])
    def create_new_question():
        # get the data from the request
        body = request.get_json()

        # check if the data is valid
        if body.get('question', None) is None:
            abort(422)
        if body.get('answer', None) is None:
            abort(422)
        if body.get('difficulty', None) is None:
            abort(422)
        if body.get('category', None) is None:
            abort(422)
        
        # create a new question
        new_question = Question(
            question=body.get('question'),
            answer=body.get('answer'),
            difficulty=body.get('difficulty'),
            category=body.get('category')
        )
        # insert the new question into the database
        new_question.insert()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
            'success': True,
            'question': current_questions,
            'total_questions': len(Question.query.all())
        })

    # endpoint to POST  to get question using search term
    @app.route('/search', methods=['POST'])
    def search_questions():
        # get the data from the request
        body = request.get_json()

        # check if the data is valid
        if body.get('searchTerm', None) is None:
            abort(422)

        # search for the question
        selection = Question.query.filter(Question.question.ilike(f'%{body.get("searchTerm")}%')).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection)
        })


    # GET endpoint to get questions based on category.
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        category = Category.query.filter_by(id=category_id).one_or_none()
        if category:
           question_in_category = Question.query.filter_by(category=str(category.id)).all()
           current_questions = paginate_questions(request, question_in_category)
           return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(question_in_category),
                'current_category': category.type
            })
        else:
            abort(404)


    # POST endpoint to get questions to play the quiz.
    @app.route('/quizzes', methods=['POST'])
    def quiz_questions():
        # get the data from the request
        body = request.get_json()
        quiz_category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')
        try:
            if(quiz_category['id'] == 0):
                selection = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                selection = Question.query.filter(Question.id.notin_(previous_questions), Question.category == quiz_category['id']).all()
            
            random_index = random.randint(0, len(selection) - 1)
            next_question = selection[random_index]

            still_questions = len(selection)
            if(still_questions == 0):
                return jsonify({
                    'success': True,
                    'question': None
                })
            else:
                return jsonify({
                    'success': True,
                    'question': next_question.format()
                })
        except:
            abort(422)
            
            

    
    # Error handlers for 400, 404, 422 and 500
    @app.errorhandler(400)
    def error_400(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def error_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(422)
    def error_not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def error_not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app
