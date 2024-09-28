#!/usr/bin/python3
"""
Unit tests for the FileStorage class
"""
import unittest
from models.base_model import BaseModel
from models.user import User
from models import storage
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test not supported')
class TestFileStorage(unittest.TestCase):
    """Test cases for FileStorage class"""

    def setUp(self):
        """Setup method to reset the storage state for each test"""
        self.clear_storage()
    
    def tearDown(self):
        """Teardown method to clean up after each test"""
        self.clear_storage()
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass
    
    def clear_storage(self):
        """Helper function to clear storage objects"""
        del_list = []
        for key in storage.all().keys():
            del_list.append(key)
        for key in del_list:
            del storage.all()[key]
    
    def test_storage_empty(self):
        """Test that storage is initially empty"""
        self.assertEqual(len(storage.all()), 0)

    def test_new_object_added(self):
        """Test that a new object is correctly added to storage"""
        new = BaseModel()
        new.save()
        storage.reload()
        self.assertIn(f"BaseModel.{new.id}", storage.all())

    def test_all_returns_dict(self):
        """Test that the all() method returns a dictionary"""
        self.assertIsInstance(storage.all(), dict)

    def test_save_creates_file(self):
        """Test that saving creates a JSON file"""
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload_loads_objects(self):
        """Test that objects are correctly reloaded from the file"""
        new = BaseModel()
        new.save()
        storage.reload()
        key = f"BaseModel.{new.id}"
        self.assertIn(key, storage.all())

    def test_reload_empty_file(self):
        """Test reloading from an empty file"""
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_nonexistent_file(self):
        """Test that reload() does nothing if the file doesn't exist"""
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass
        self.assertIsNone(storage.reload())

    def test_key_format(self):
        """Test that keys in storage are formatted correctly"""
        new = BaseModel()
        new.save()
        expected_key = f"BaseModel.{new.id}"
        self.assertIn(expected_key, storage.all())

    def test_user_class_in_storage(self):
        """Test that a User object is stored and loaded properly"""
        user = User(email="test@example.com", first_name="John", last_name="Doe", password="password")
        user.save()
        storage.reload()
        key = f"User.{user.id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].email, "test@example.com")
        self.assertEqual(storage.all()[key].first_name, "John")
        self.assertEqual(storage.all()[key].last_name, "Doe")
        self.assertEqual(storage.all()[key].password, "password")

    def test_non_existing_attribute(self):
        """Test that nonexistent attributes are not included after save/reload"""
        user = User()
        user.save()
        storage.reload()
        key = f"User.{user.id}"
        self.assertFalse(hasattr(storage.all()[key], "non_existing_attribute"))

    def test_empty_object_storage(self):
        """Test that an empty object can be saved and loaded"""
        user = User()
        user.save()
        storage.reload()
        key = f"User.{user.id}"
        self.assertIn(key, storage.all())

    def test_instance_initialization_with_kwargs(self):
        """Test instance initialization with kwargs on reload"""
        user = User(email="test@example.com", first_name="John", last_name="Doe", password="password")
        user.save()
        storage.reload()
        key = f"User.{user.id}"
        loaded_user = storage.all()[key]
        self.assertEqual(loaded_user.email, "test@example.com")
        self.assertEqual(loaded_user.first_name, "John")
        self.assertEqual(loaded_user.last_name, "Doe")
        self.assertEqual(loaded_user.password, "password")


if __name__ == "__main__":
    unittest.main()
