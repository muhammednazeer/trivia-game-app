import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'docker', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is the capital of Peru?',
            'answer': 'Lima',
            'difficulty': 2,
            'category': 3
        }

        self.quiz_game = {
            'previous_questions': [6, 7],
            'quiz_category': {
                'type': 'Sports',
                'id': '6'
            }
        }

        self.bad_quiz_game = {
            'previous_questions': [6, 7],
            'quiz_category': {
                'type': 'Sports',
                'id': '666'
            }
        }

        self.search_term = {'searchTerm': 'Burton'}

        self.no_search_term = {'searchTerm': ''}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(len(data['categories']), 0)

    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_sent_requesting_beyond_valid_page(self):
        response = self.client().get('/questions?page=100')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        question = Question(
            question=self.new_question['question'],
            answer=self.new_question['answer'],
            category=self.new_question['category'],
            difficulty=self.new_question['difficulty']
        )
        question.insert()
        question_id = question.id
        questions_before = Question.query.all()
        response = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(response.data)
        questions_after = Question.query.all()
        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertTrue(len(questions_before) - len(questions_after) == 1)
        self.assertEqual(question, None)

    def test_404_delete_question(self):
        question_id = 666
        response = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_create_new_question(self):
        questions_before = Question.query.all()
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)
        questions_after = Question.query.all()
        question = Question.query.filter_by(id=data['created']).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(questions_after) - len(questions_before) == 1)
        self.assertIsNotNone(question)

    def test_422_if_question_creation_fails(self):
        questions_before = Question.query.all()
        response = self.client().post('/questions', json={})
        data = json.loads(response.data)
        questions_after = Question.query.all()

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(questions_after) == len(questions_before))

    def test_search_questions(self):
        response = self.client().post('/questions', json=self.search_term)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)

    def test_no_term_search_questions(self):
        response = self.client().post('/questions', json=self.no_search_term)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_get_questions_by_category(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['questions']), 0)

    def test_422_if_questions_by_category_fails(self):
        response = self.client().get('/categories/322/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_quiz_game(self):
        response = self.client().post('/quizzes', json=self.quiz_game)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 6)
        self.assertNotEqual(data['question']['id'], 6)
        self.assertNotEqual(data['question']['id'], 7)

    def test_error_category_quiz_game(self):
        response = self.client().post('/quizzes', json=self.bad_quiz_game)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
