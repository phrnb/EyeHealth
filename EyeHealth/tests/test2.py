
import unittest
from userService import UserService

class TestUserService(unittest.TestCase):

    def setUp(self):
        self.user_service = UserService()

    def test_authenticate_success(self):
        result = self.user_service.authenticate("user1", "password123")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["message"], "Authenticated successfully")

    def test_authenticate_failure_invalid_password(self):
        result = self.user_service.authenticate("user1", "wrongpassword")
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Invalid username or password")

    def test_authorize_success(self):
        result = self.user_service.authorize("user1", "admin")
        self.assertTrue(result)

    def test_authorize_failure_invalid_role(self):
        result = self.user_service.authorize("user2", "admin")
        self.assertFalse(result)

    def test_authorize_failure_user_not_found(self):
        result = self.user_service.authorize("nonexistent_user", "admin")
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
