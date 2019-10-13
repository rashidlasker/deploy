Assignment 5: Unit tests and Continuous Integration
========

[Week 5 slides](https://docs.google.com/presentation/d/1Ifrnjn7lQRDCmycdPIRFsGi7QckuuqXb_my4TQA0LbU/edit?usp=sharing)

This week you'll be learning how to write and run unit tests in Django, as well as how to add these tests to a continuous integration pipeline that will ensure your codebase stays healthy.

Unit testing in Django
----

## Writing tests

In your Django app directory (the same directory that contains `models.py` and `views.py`), create a `tests.py` file.

In `tests.py`, you will write 5 unit tests that will test the correctness of your application. Unit tests are small tests that each verify whether or not a small part of your app is behaving correctly. Ideally, a unit is the smallest testable part of any software, but units are sometimes hard to identify. In general, it is a good idea to test each endpoint of your application. Your tests should verify that each endpoint behaves as expected.

```python
from django.test import TestCase, Client
from django.urls import reverse
from rebu.models import user, meal
from urllib.parse import urlencode
from django.core.management import call_command

class test_user(TestCase):

    # Load test data from database fixture.
    def setUp(self):
        call_command('loaddata', 'rebu/fixtures/rebu/rebu_testdata.json', verbosity = 0)

    # Unit test. Verify that user with id 1 already exists. (This user is in our fixture data.)
    def test_verify_user_exists(self):
        response = self.client.get(reverse('user', args = [1]))
        self.assertEqual(response.status_code, 200)

    # Verify that user with id 2 has name 'Rashid'. (This user is in our fixture data.)
    def test_existing_user(self):
        response = self.client.get(reverse('user', args = [2]))
        self.assertContains(response, 'true')
        self.assertContains(response, 'Rashid')

    # Test API endpoint that will create a new user, not in our fixture data.
    def test_new_user(self):
        data = {
                "first_name": "John",
                "last_name": "Smith",
                "street": "107N Piedmont Ave",
                "zip_code": "22904",
                "state": "VA",
                "country": "US",
                "bio": "bio",
                "links": "docker.com",
                "language": "English",
                "gender": "Male",
                "password": "password",
                "username": "js4be"
               }

        response_post = self.client.post('/api/v1/users/create/', data)
        response = self.client.get('/api/v1/users/4/')
        self.assertContains(response_post, 'true')
        self.assertContains(response, 'true')

    # Test endpoint that updates user data.
    def test_update_user(self):
        data = {"first_name": "Brian"}
        response_post = self.client.post('/api/v1/users/1/', data)
        response = self.client.get('/api/v1/users/1/')
        self.assertContains(response_post, 'true')
        self.assertContains(response, 'true')
        self.assertContains(response, 'Brian')

    # Test endpoint that deletes user.
    def test_delete_user(self):
        response = self.client.delete('/api/v1/users/3/')
        self.assertContains(response, 'true')
        response_false = self.client.get('/api/v1/users/3/')
        self.assertContains(response_false, 'false')

    def tearDown(self):
        pass
```

You may also wish to write tests that test edge cases of your application logic. Consider this example test:

```python
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
```

You may not expect Questions to be published with pub_dates in the future. However, this very well may happen since you can't control what consumers of your API will do. You should either prohibit future pub_dates or test that future pub_dates work correctly.

Useful links:
- [Django tutorial testing](https://docs.djangoproject.com/en/2.2/intro/tutorial05/)
- [Django testing overview](https://docs.djangoproject.com/en/2.2/topics/testing/overview/)

## Running tests

It's simple. Running `python manage.py test <app_directory>` in the appropriate docker container will run all files in `/<app_directory>` whose filenames start with `test`. This means that `tests.py` will be run, as well as any other test files, should you decide to split your tests into multiple files (this is a good practice that helps when the number of test cases you write for your app grows larger).

Continuous Integration using TravisCI
----
Continuous integration is a dev ops practice widely used within the industry. It involves automated tests and scripts that run before you check-in code to maximize code quality and health. This allows developers to detect errors quickly and before they are introduced into the shared codebase.

The CI platform that we will be using is TravisCI, because of its integrations with GitHub. Here are the Getting Started docs: [https://docs.travis-ci.com/user/tutorial/](https://docs.travis-ci.com/user/tutorial/). We have also included a sample `.travis.yml` file to help you get started. 


What to turn in
---------------

For this project, we expect you to write 5 unit tests and make TravisCI a part of your GitHub repository workflow. Please submit screenshots of your TravisCI dashboard showing a completed build after you get everything working.

Finally, we strongly encourage you to take time to demo in the office hours or in lab. We want to make sure not only you are writing code that works but also code that is of best practices.
