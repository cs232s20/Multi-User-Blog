import sqlite3
import os
from datetime import datetime
from sqlite3 import IntegrityError


def row_to_dict_or_false(cur):
    """
    Given a cursor that has just been used to execute a query, try to fetch one
    row. If the there is no row to fetch, return False, otherwise return a
    dictionary representation of the row.

    :param cur: a cursor that has just been used to execute a query
    :return: a dict representation of the next row, or False
    """
    row = cur.fetchone()

    if row is None:
        return False
    else:
        return dict(row)


def hash_string(password):
    """
    Given a string, this function hashes the string.

    :param password: a password(string) to be hashed
    :return: hashed value of password
    """
    return hash(password)


class BlogPost:

    def __init__(self, sqlite_filename):
        """
        Creates a connection to the database, and creates tables if the
        database file did not exist prior to object creation.

        :param sqlite_filename: the name of the SQLite database file
        """
        if os.path.isfile(sqlite_filename):
            create_tables = False
        else:
            create_tables = True

        self.conn = sqlite3.connect(sqlite_filename)
        self.conn.row_factory = sqlite3.Row

        cur = self.conn.cursor()
        cur.execute('PRAGMA foreign_keys = 1')
        cur.execute('PRAGMA synchronous = NORMAL')

        if create_tables:
            self.create_tables()

    def create_tables(self):
        """
        Create the tables blog, author and password.
        """

        cur = self.conn.cursor()
        cur.execute('CREATE TABLE blog(blog_id INTEGER PRIMARY KEY, '
                    '    title TEXT, subtitle TEXT, content TEXT, date TEXT,  '
                    '    author_id INTEGER, '
                    'FOREIGN KEY (author_id) REFERENCES author(author_id)) ')

        cur.execute('CREATE TABLE author(author_id INTEGER PRIMARY KEY, '
                    '                     name TEXT UNIQUE) ')

        cur.execute('CREATE TABLE password(password_id INTEGER PRIMARY KEY,'
                    '                       author_id INTEGER, '
                    '                      password TEXT, '
                    'FOREIGN KEY (author_id) REFERENCES author(author_id)) ')

        self.conn.commit()

    def insert_blog(self, title, subtitle, author, content):
        """
        Inserts a blog into the database. If the author is not already in
        database, it returns False.

        :param title: title for the post
        :param subtitle: subtitle for the post
        :param author: author of the post
        :param content: content of the post
        :return: a dict representing the blog or False

        """

        now = datetime.now()
        date = now.strftime("%B %d, %Y || %I:%M%p")
        author_dict = self.get_author_by_name(author)
        if author_dict is not False:
            author_id = author_dict['author_id']

            cur = self.conn.cursor()

            query = ('INSERT INTO blog(title, subtitle, content, date, '
                     '                 author_id) '
                     'VALUES(?, ?, ?, ?, ?) ')
            cur.execute(query, (title, subtitle, content, date, author_id))
            self.conn.commit()
            return self.get_blog_by_id(cur.lastrowid)
        else:
            return False

    def get_blog_by_id(self, blog_id):
        """
        Given a blog_id, return a dictionary representation of the blog post
        or False if there is no post with that blog_id.

        :param blog_id: blog_id for a post
        :return: a dict representing the blog.

        """
        cur = self.conn.cursor()
        query = ('SELECT blog_id, title, subtitle, content, date, author_id '
                 'FROM blog '
                 'WHERE blog.blog_id = ? ')

        cur.execute(query, (blog_id,))
        return row_to_dict_or_false(cur)

    def get_all_posts(self):
        """
        Return a list of dictionaries representing all of the posts in the blog
        database.

        :return: a list of dict objects representing blog posts
        """
        cur = self.conn.cursor()

        query = 'SELECT blog.blog_id as id, blog.title as title, ' \
                'blog.subtitle as subtitle, ' \
                'blog.content as content, blog.date as date, ' \
                'author.name as author  ' \
                'FROM blog, author ' \
                'WHERE blog.author_id = author.author_id ' \
                'ORDER BY blog_id DESC '

        posts = []
        cur.execute(query)

        for row in cur.fetchall():
            posts.append(dict(row))

        return posts

    def sign_up_entry(self, author, password):
        """
        Given a new author's name and password, enter the user in
        database and return a dictionary representation of the new user. False
        if the user already exists.

        :param author: name of author
        :param password: password of author
        :return: a dictionary representing the new user
        """
        try:
            cur = self.conn.cursor()
            author_dict = self.__insert_author(author)
            author_id = author_dict['author_id']
            self.__insert_password(author_id, password)
            self.conn.commit()
            return self.get_author_by_id(author_id)

        except TypeError:
            return False

    def __insert_author(self, author):
        """
        Private method to enter a user in database and return a dictionary
        representation of the new user. False if the user already exists.

        :param author: name of author
        :return: a dictionary representing the new user
        """

        try:
            cur = self.conn.cursor()
            query = 'INSERT INTO author(name) VALUES(?)'
            cur.execute(query, (author,))
            self.conn.commit()
            return self.get_author_by_name(author)

        except IntegrityError:
            return False

    def get_author_by_name(self, name):
        """
        Given an existing author's name, return a dictionary representation
        of the user. False if the user doesn't exist.

        :param name: name of author
        :return: a dictionary representing the author
        """

        cur = self.conn.cursor()
        query = 'SELECT author_id , name FROM author WHERE name = ? '
        cur.execute(query, (name,))
        return row_to_dict_or_false(cur)

    def get_author_by_id(self, id_num):
        """
        Given an existing author's id, return a dictionary representation of
        the user. False if the user doesn't exist.

        :param id_num: id of author
        :return: a dictionary representing the author
        """

        cur = self.conn.cursor()
        query = 'SELECT author_id , name FROM author WHERE author_id = ?'
        cur.execute(query, (id_num,))
        return row_to_dict_or_false(cur)

    def __insert_password(self, author_id, password):
        """
        Private method to enter a password for a particular user in the
        database and return True if successful .
        :param author: name of author
        :return: True if successful
        """
        cur = self.conn.cursor()
        hashed_password = hash_string(password)
        query = ('INSERT INTO password(author_id, password) '
                 'VALUES(?, ?)')

        cur.execute(query, (author_id, hashed_password))
        self.conn.commit()
        return True

    def password_check(self, user, password):
        """
        Given a new author's name and password, check whether the
        user in database corresponds to the password and return a dictionary
        representation of the new user. False is password doesn't match.

        :param user: name of user
        :param password: password of user
        :return: a dictionary representing the new user
        """

        try:
            cur = self.conn.cursor()
            author_dict = self.get_author_by_name(user)
            author_id = author_dict['author_id']
            hashed_password = hash_string(password)

            query = ('SELECT password_id FROM password '
                     'WHERE password.author_id = ?'
                     'AND password.password = ? ')
            cur.execute(query, (author_id, hashed_password))
            return row_to_dict_or_false(cur)
        except TypeError:
            return False

    def update_password(self, user, old_password, new_password):
        """
        Changes the password of an existing user to a new one in the
        database. Returns False is user is not found.

        :param user: name of the user
        :param old_password: old password of user to be replaced
        :param new_password: new password that replaces the old one
        :return: a dictionary representing the new user
        """
        try:
            cur = self.conn.cursor()
            author_dict = self.get_author_by_name(user)
            author_id = author_dict['author_id']
            condition = self.password_check(user, old_password)

            if condition is not False:
                hashed_password = hash_string(new_password)
                query = ('UPDATE password '
                         'SET password = ? '
                         'WHERE password.author_id = ? ')
                cur.execute(query, (hashed_password, author_id))
                self.conn.commit()
                return True
            else:
                return condition

        except TypeError:
            return False


if __name__ == '__main__':

    db = BlogPost('blog.sqlite')
