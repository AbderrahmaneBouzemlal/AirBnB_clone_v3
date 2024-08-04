#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
from unittest.mock import patch, MagicMock
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


if models.storage_t == "db":
    class TestDBStorage(unittest.TestCase):
        """Test the DBStorage class"""
        @classmethod
        def setUpClass(cls):
            """Setup a test instance of DBStorage"""
            cls.storage = DBStorage()
            cls.storage.reload()

        def setUp(self):
            """Set up the test method environment"""
            # Mock the session
            self.mock_session = MagicMock()
            self.storage._DBStorage__session = self.mock_session

        def tearDown(self):
            """Tear down the test method environment"""
            # Reset mocks
            self.mock_session.reset_mock()

        def test_all_returns_dict(self):
            """Test that all returns a dictionary"""
            all_objs = self.storage.all()
            self.assertIsInstance(
                all_objs,
                dict,
                "all() should return a dictionary"
                )

        def test_all_no_class(self):
            """Test that all returns all rows when no class is passed"""
            # Simulate some objects
            mock_query = self.mock_session.query.return_value
            mock_query.all.return_value = [
                MagicMock(spec=BaseModel),
                MagicMock(spec=BaseModel)
            ]

            # Run test
            all_objs = self.storage.all()
            self.assertEqual(
                len(all_objs),
                2,
                "all() should return all\
                objects in the session")

        def test_all_with_class(self):
            """Test that all returns all rows
            of a specific class
            when class is passed"""
            # Create a mock query response
            mock_obj1 = MagicMock(spec=City)
            mock_obj2 = MagicMock(spec=City)
            mock_obj1.id = '123'
            mock_obj2.id = '456'
            mock_obj1.__class__.__name__ = 'City'
            mock_obj2.__class__.__name__ = 'City'

            # Simulate session query
            mock_query = self.mock_session.query.return_value
            mock_query.all.return_value = [mock_obj1, mock_obj2]

            # Call all with City class
            all_cities = self.storage.all(City)
            self.assertEqual(
                len(all_cities),
                2,
                "all(City) should return all city objects")
            self.assertIn(
                'City.123',
                all_cities,
                "all(City) should contain City.123")
            self.assertIn(
                'City.456',
                all_cities,
                "all(City) should contain City.456"
                )

        def test_new(self):
            """Test that new adds an object to the database"""
            # Create a mock object
            new_obj = MagicMock(spec=BaseModel)
            new_obj.id = "c56a8a10-00f5-4673-8535-2d08795a8cf3"
            new_obj.__class__.__name__ = "City"

            # Call new()
            self.storage.new(new_obj)

            # Assert the object is added to the session
            self.mock_session.add.assert_called_once_with(new_obj)

        def test_save(self):
            """Test that save properly saves objects to the database"""
            # Call save()
            self.storage.save()

            # Assert the commit method is called
            self.mock_session.commit.assert_called_once()

        def test_delete(self):
            """Test that delete removes an object from the database"""
            # Create a mock object
            del_obj = MagicMock(spec=BaseModel)

            # Call delete()
            self.storage.delete(del_obj)

            # Assert the object is deleted from the session
            self.mock_session.delete.assert_called_once_with(del_obj)

        # def test_get(self):
        #     """Test that get returns
        #     the correct object based on
        #     class and ID"""
        #     # Create a mock object
        #     mock_obj = MagicMock(spec=BaseModel)
        #     mock_obj.id = "c56a8a10-00f5-4673-8535-2d08795a8cf3"
        #     mock_obj.__class__.__name__ = "City"
        #     self.storage.new(mock_obj)

        #     # Simulate query filter and first method
        #     mock_query = self.mock_session.query.return_value
        #     mock_query.filter.return_value.first.return_value = mock_obj

        #     # Retrieve the object
        #     result = self.storage.get(
        #         City,
        #         "c56a8a10-00f5-4673-8535-2d08795a8cf3")
        #     self.assertEqual(
        #         result,
        #         mock_obj,
        #         "get() should return the correct\
        #         object based on class and ID")

        def test_get_invalid_id(self):
            """Test get with invalid ID"""
            # Simulate query returning None
            mock_query = self.mock_session.query.return_value
            mock_query.filter.return_value.first.return_value = None

            # Retrieve the object with an invalid ID
            result = self.storage.get(City, "invalid_id")
            self.assertIsNone(
                result,
                "get() should return None\
                for an invalid ID")

        def test_count(self):
            """Test that count returns the
            correct number of objects
            for a given class"""
            # Simulate query count return value
            mock_query = self.mock_session.query.return_value
            mock_query.count.return_value = 5

            # Get count
            count = self.storage.count(City)
            self.assertEqual(
                count,
                5,
                "count() should return the correct\
                number of objects for a given class"
                )

        def test_count_all(self):
            """Test that count returns the correct number of all objects"""
            # Simulate query count return value for all classes
            self.mock_session.query().count.side_effect = [2, 3, 4, 1, 2, 3]

            # Get total count
            total_count = self.storage.count()
            self.assertEqual(
                total_count,
                15,
                "count() should return the correct\
                total number of objects for all classes"
                )

        def test_reload(self):
            """Test that reload recreates the database session"""
            # Mock the sessionmaker and scoped_session
            with patch(
                'models.engine.db_storage.sessionmaker'
                ) as mock_sessmaker, \
                patch(
                    'models.engine.db_storage.scoped_session'
                    ) as mock_scoped_sess:
                # Configure mock return value
                mock_sess_instance = MagicMock()
                mock_sessmaker.return_value = mock_sess_instance
                mock_scoped_sess.return_value = MagicMock()

                # Call reload
                self.storage.reload()

                # Assert that sessionmaker and scoped_session were called
                mock_sessmaker.assert_called_once_with(
                    bind=self.storage._DBStorage__engine,
                    expire_on_commit=False
                    )
                mock_scoped_sess.assert_called_once_with(mock_sess_instance)

        def test_close(self):
            """Test that close properly calls remove on the session"""
            # Call close
            self.storage.close()

            # Assert that the remove method was called
            self.mock_session.remove.assert_called_once()
