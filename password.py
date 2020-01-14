"""
This code will wait for the password input from console.
Verify the password with the existing MD5 encoded one.
Added function to create new users or delete existing from database.
"""

# getpass package let user input password in console invisibly.
import _sqlite3
import hashlib
import os
import time


class DbActions:
    def __init__(self, dbfile, dbtable):
        self._dbfile = dbfile
        self._dbtable = dbtable
        # Create Database connection & cursor for later use.
        if os.path.exists(self._dbfile):
            self.conn = _sqlite3.connect(self._dbfile)
            self.cursor = self.conn.cursor()
            print('Database connection established.')
        else:
            # If the database file doesn't exist then quit.
            exit('Database do not exist.')

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        print('Database connection closed.')

    @property
    def get_dbfilename(self):
        return self._dbfile

    def set_dbfilename(self, dbfile):
        self._dbfile = dbfile

    def add(self, username, password):
        self.cursor.execute('select max(serial) from USERS')
        current_serial = self.cursor.fetchone()
        serial = current_serial[0] + 1
        timeNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        values = (username, password, serial, timeNow)
        try:
            self.cursor.execute("insert into USERS values (?, ?, ?, ?)", values)
            self.conn.commit()
            return 1
        except:
            return 0

    def verify(self, username, password):
        self.cursor.execute('select PwdMD5 from USERS where Username=?', (username))
        _real_password = self.cursor.fetchone()
        if _real_password[0] == password:
            return 1
        else:
            return 0

    def delete_user(self, username, password):
        self.cursor.execute('select PwdMD5 from USERS where Username=?', (username))
        _real_password = self.cursor.fetchone()
        if _real_password[0] == password:
            try:
                self.cursor.execute('DELETE FROM USERS WHERE Username=?', username)
                self.conn.commit()
                return 1
            except:
                return 0
        else:
            return 0


class User(object):
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._dbfilename = 'users.db'
        self._dbtable = 'USERS'

    @property
    def username(self):
        return self._username

    def add_user(self):
        new_user = DbActions(self._dbfilename, self._dbtable)
        result = new_user.add(self._username, self.md5_encoding(self._password))
        if result:
            print('User %s created!' % self._username)
        else:
            print('User creation failed.')

    def user_verify(self):
        user = DbActions(self._dbfilename, self._dbtable)
        result = user.verify(self._username, self.md5_encoding(self._password))
        if result:
            print('User %s is correct!' % self._username)
        else:
            print('User verification failed.')

    def delete_user(self):
        user = DbActions(self._dbfilename, self._dbtable)
        result = user.delete_user(self._username, self.md5_encoding(self._password))
        if result:
            print('User %s deleted!' % self._username)
        else:
            print('User deletion failed.')

    def md5_encoding(self, _str):
        str_original = _str
        md5_str = hashlib.md5()
        md5_str.update(str_original.encode(encoding='utf-8'))
        return md5_str.hexdigest()


if __name__ == "__main__":
    print(
        'Select what action you would like to perform: \n'
        '1. Create new user \n'
        '2. Verify this user \n'
        '3. Delete this user \n'
    )
    print('Make your choice:')
    choice = int(input())
    print('Username:')
    username = input().strip()
    print('Password:')
    password = input().strip()
    if choice == 1:
        newUser = User(username, password)
        newUser.add_user()
    elif choice == 2:
        verifyUser = User(username, password)
        verifyUser.user_verify()
    elif choice == 3:
        deleteUser = User(username,password)
        deleteUser.delete_user()
    else:
        print('You made the wrong choice.')
