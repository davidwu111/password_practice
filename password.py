"""
This code will wait for the password input from console.
Verify the password with the existing MD5 encoded one.
"""

# getpass package let user input password in console invisibly.
import _sqlite3


class User(object):
    def __init__(self, username, password):
        self._username = username
        self._password = password

    @property
    def username(self):
        return self._username

    def add_user(self):

    def user_verify(self):

    def delete_user(self):



if __name__ == "__main__":
    print('start')

