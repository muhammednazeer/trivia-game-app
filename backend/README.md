# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## API Reference

Getting Started

- Backend Base URL: http://127.0.0.1:5000/
- Authentication: Authentication or API keys are not used in the project yet.

### Error handling

Errors are returned in the following json format:

```JSON
{
    "success": "False",
    "error": 422,
    "message": "Unprocessable entity",
}
```

The error codes currently returned are:

- 400 – bad request
- 404 – resource not found
- 422 – unprocessable
- 500 – internal server error

### Endpoints

#### GET `/categories`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Returns: An object with these keys:
  - `categories`: Contains a object of:
    - key: `category_id`
    - value: name of category
  - `success`: The success flag

```JSON
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```

#### GET `/categories`

- Fetches all the questions paginated and a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category, and the total of questions.
- Returns: An object with these keys:
  - `categories`: Contains a object of:
    - key: `category_id`
    - value: name of category
  - `questions`: A list of questions objects, paginated (10) with the structure:
    - `answer`: string,
    - `category`: number,
    - `difficulty`: number,
    - `id`: number,
    - `question`: string
  - `success`: The success flag
  - `total_questions`: The total of questions

```JSON
{
    "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
    },
    "questions": [
        {
          "answer": "Apollo 13",
          "category": 5,
          "difficulty": 4,
          "id": 2,
          "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
          "answer": "Tom Cruise",
          "category": 5,
          "difficulty": 4,
          "id": 4,
          "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
          "answer": "Maya Angelou",
          "category": 4,
          "difficulty": 2,
          "id": 5,
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
          "answer": "Edward Scissorhands",
          "category": 5,
          "difficulty": 3,
          "id": 6,
          "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
          "answer": "Muhammad Ali",
          "category": 4,
          "difficulty": 1,
          "id": 9,
          "question": "What boxer's original name is Cassius Clay?"
        },
        {
          "answer": "Brazil",
          "category": 6,
          "difficulty": 3,
          "id": 10,
          "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
          "answer": "Uruguay",
          "category": 6,
          "difficulty": 4,
          "id": 11,
          "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
          "answer": "George Washington Carver",
          "category": 4,
          "difficulty": 2,
          "id": 12,
          "question": "Who invented Peanut Butter?"
        },
        {
          "answer": "Lake Victoria",
          "category": 3,
          "difficulty": 2,
          "id": 13,
          "question": "What is the largest lake in Africa?"
        },
        {
          "answer": "The Palace of Versailles",
          "category": 3,
          "difficulty": 3,
          "id": 14,
          "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 19
}
```

### DELETE `/questions/:question_id/`

- Delete question using a `question_id` parameter
- Request arguments:
  - `question_id` (number): The question id
- Returns: An object with theses keys:
  - `deleted` The ID of the question deleted.
  - `success` The success flag
  - `total_questions` The total of questions remaining

```JSON
{
    "deleted": 4,
    "success": true,
    "total_questions": 17
}
```

### POST `/questions`

- Create a new question.
- Request arguments:
  - `question`: (string)
  - `answer`: (string)
  - `difficulty`: (string)
  - `category`: (string)

```JSON
{
    "question": "What is the capital of France?",
    "answer": "Paris",
    "difficulty" : 2,
    "category": 3
}
```

- Returns: An object with theses keys:
  - `created` Contains the ID of the question created.
  - `success` The success flag
  - `total_questions` The total of questions remaining

```JSON
{
    "created": 28,
    "success": true,
    "total_questions": 19
}
```

### POST `/questions` (search)

- Search for a question that contains the search term inserted.
- Request arguments:
  - `searchTerm`: (string)

```JSON
{
    "searchTerm": "Mirrors"
}
```

- Returns: An object with theses keys:
  - `questions` Questions that contains the term searched.
  - `success` The success flag
  - `total_questions` The total of questions with the term searched

```JSON
{
    "questions": [
        {
          "answer": "The Palace of Versailles",
          "category": 3,
          "difficulty": 3,
          "id": 14,
          "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

### GET `/categories/:category_id/questions`

- Fetches a list of questions based on category.
- Request arguments:
  - `category_id`: (number)
- Returns: An object with these keys:
  - `current_category`: The current category
  - `questions`: A list of questions
  - `success`: The success flag
  - `total_questions`: The total of questions

#### Example with `/categories/4/questions`

```JSON
{
  "current_category": {
    "id": 4,
    "type": "History"
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

### POST /quizzes

- Fetches a question to play the quiz.
- Request arguments:
  - `quiz_category` (dictionary): The quiz category with the type and the id.
  - `previous_ids`: (list of strings)

```JSON
{
    "previous_questions": [],
    "quiz_category": {
        "type": "Entertainment",
        "id": 5
    }
}
```

- Returns: An object with these keys:
  - `question`: The question to play
  - `success`: The success flag

```JSON
{
  "question": {
    "answer": "Edward Scissorhands",
    "category": 5,
    "difficulty": 3,
    "id": 6,
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  },
  "success": true
}
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Authors

- Muhammed Hussaini worked on the API and tests.
- Udacity provided the starter files for the project including the frontend
