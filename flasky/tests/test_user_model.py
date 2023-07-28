import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        """
        Checks if the passowrd setter property correctly sets the
        password_hash attr of the user class when a password is
        assigned to it.
        """
        u = User(password = 'cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        """
        Ensures that the password getter property raises an Attr Error
        when trying to access the plaintext password directly.
        This test confirms that the password attr is not readable.
        """
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        """
        The test verifies that the verify_password method correctly compares
        a given plaintext password with the hashed password stored in the
        user Instance
        """
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        """
        Checks if the password salts are random for different instances of the
        user class.This test is designed to ensure that when crearting two
        different user instances with the same plaintext password, their
        resulting password hashes(including salts) are different.
        """
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)
