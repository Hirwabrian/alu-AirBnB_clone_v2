import unittest
from models.user import User
from models import storage
from models.engine.db_storage import DBStorage
import os

class TestDBStorage(unittest.TestCase):
    def setUp(self):
        """ Set up for DBStorage tests. """
        # Clear the database or set up a test database
        storage.reload()  # Ensure storage is empty before tests
        self.new_user = User(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            password="securepassword"
        )
        storage.new(self.new_user)  # Add user to the storage
        self.new_user.save()  # Persist the user to the database

    def tearDown(self):
        """ Clean up after tests. """
        # Clean up the database
        storage.delete(self.new_user)
        storage.save()  # Save changes

    def test_all_users(self):
        """ Test that all users can be retrieved. """
        users = storage.all(User)  # Retrieve all users
        self.assertIn(f'User.{self.new_user.id}', users)  # Check if the new user is present

    def test_get_user(self):
        """ Test getting a user by ID. """
        user = storage.get(User, self.new_user.id)
        self.assertIsNotNone(user)  # User should not be None
        self.assertEqual(user.email, self.new_user.email)  # Check email matches

    def test_count_users(self):
        """ Test counting the number of users. """
        count_before = storage.count(User)  # Count before adding new user
        self.assertEqual(count_before, 1)  # There should be one user
        new_user2 = User(email="another@example.com", first_name="Jane", last_name="Smith", password="anotherpassword")
        storage.new(new_user2)
        new_user2.save()  # Save second user
        count_after = storage.count(User)  # Count after adding second user
        self.assertEqual(count_after, 2)  # Should now be two users

if __name__ == "__main__":
    unittest.main()
