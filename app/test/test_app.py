import unittest
import json
from app import app


class TestAppEndpoints(unittest.TestCase):
    user_id = ""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_01_create_user(self):
        response = self.app.post('/api/v1.0/user', json={
            "name": "Test User",
            "description": "Test user description",
            "mbti": "INTJ",
            "enneagram": "9w3",
            "variant": "sp/so",
            "tritype": 541,
            "socionics": "SEE",
            "sloan": "RCOEN",
            "psyche": "FEVL",
            "temperaments": "Phlegmatic [Dominant]",
            "image": "https://example.com/image.png"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', json.loads(response.data))
        self.__class__.user_id = response.get_json()["id"]

    def test_02_get_user(self):
        response = self.app.get(f'/api/v1.0/user/{self.__class__.user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({
            "_id": self.__class__.user_id,
            "name": "Test User",
            "description": "Test user description",
            "mbti": "INTJ",
            "enneagram": "9w3",
            "variant": "sp/so",
            "tritype": 541,
            "socionics": "SEE",
            "sloan": "RCOEN",
            "psyche": "FEVL",
            "temperaments": "Phlegmatic [Dominant]",
            "image": "https://example.com/image.png"
        }, response.get_json())

    def test_03_post_comment(self):
        response = self.app.post(
            f'/api/v1.0/user/{self.__class__.user_id}/comment',
            json={
                "from_user_id": "65bc7bc191563e032e184fc0",
                "mbti": "INTP",
                "body": "A simple test comment"
            }
        )

        self.assertEqual(response.status_code, 201)

    def test_04_get_comments(self):
        response = self.app.get(
            f'/api/v1.0/user/{self.__class__.user_id}/comments'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json()["comments"], list)

    def test_05_like_comment(self):
        # comment_id will not exist and will return a not found error
        response = self.app.post(
            f'/api/v1.0/user/{self.__class__.user_id}/comment/test_comment_id',
            json={"from_user_id": "65bc16d9de8ff7fcb049541b"}
        )
        self.assertEqual(response.status_code, 404)

    def test_06_unlike_comment(self):
        # comment_id will not exists and will return an error
        response = self.app.delete(
            f'/api/v1.0/user/{self.__class__.user_id}/comment/test_comment_id',
            json={"from_user_id": "65bc16d9de8ff7fcb049541b"}
        )
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
