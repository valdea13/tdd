"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status


class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update a counter and increment the value"""
        post_result = self.client.post('/counters/car')
        self.assertEqual(post_result.status_code, status.HTTP_201_CREATED)

        updated_result = self.client.put('/counters/car')
        self.assertEqual(updated_result.status_code, status.HTTP_200_OK)

        self.assertNotEqual(updated_result.json['car'], post_result.json['car'])

    def test_read_a_counter(self):
        """It reads a counter"""
        post_result = self.client.post('/counters/far')
        self.assertEqual(post_result.status_code, status.HTTP_201_CREATED)

        get_result = self.client.get('/counters/far')
        self.assertEqual(get_result.status_code, status.HTTP_200_OK)

        self.assertEqual(get_result.json['far'], post_result.json['far'])

        updated_result = self.client.put('/counters/far')
        self.assertEqual(updated_result.status_code, status.HTTP_200_OK)

        get_result = self.client.get('/counters/far')
        self.assertEqual(get_result.status_code, status.HTTP_200_OK)

        self.assertEqual(get_result.json['far'], updated_result.json['far'])


    def test_delete_a_counter(self):
        """It deletes a counter"""
        post_result = self.client.post('/counters/tar')
        self.assertEqual(post_result.status_code, status.HTTP_201_CREATED)

        delete_result = self.client.delete('/counters/tar')
        self.assertEqual(delete_result.status_code, status.HTTP_204_NO_CONTENT)

        get_result = self.client.get('/counters/tar')
        self.assertEqual(get_result.status_code, status.HTTP_404_NOT_FOUND)
