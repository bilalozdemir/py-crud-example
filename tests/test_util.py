import unittest
import base64
import os

from api import util

class TestUtilityFunctions(unittest.TestCase):

    def test_jwt_decode(self):
        _username = 'asuperuser'
        jwt_token = util.jwt_encode(_username)
        self.assertEqual(_username, util.jwt_decode(jwt_token)['username'])

    def test_check_email_validity(self):
        _valid_mail = "a@b.c"
        self.assertTrue(util.check_email_validity(_valid_mail))
        del _valid_mail
        _invalid_mails = ["abcde", "a@bcd", "abc.d", "a@.bc", "@.", "ab@?."] # etc...
        for _mail in _invalid_mails:
            with self.subTest(i=_mail):
                self.assertFalse(util.check_email_validity(_mail))

    def test_check_password_safety(self):
        _valid_password = 'SUP3RS@F3P@55W0Rd'
        self.assertEqual(_valid_password, util.check_password_safety(_valid_password))
        del _valid_password
        _invalid_passwords = ['', '1234567', 'abcdefgh', 'ABCDEFGH', 'Abcdefgh', 'Abcdefg!', 'Abcdefg1', 'Abcdef1]', 'Abcde1!ç']
        for _password in _invalid_passwords:
            with self.subTest(i=_password):
                with self.assertRaises(AssertionError):
                    util.check_password_safety(_password)

    def test_check_password(self):
        _password = 'SUP3RS@F3P@55W0Rd'
        _hashed_password = util.hash_password(_password)
        self.assertTrue(util.check_password(_password, _hashed_password))
