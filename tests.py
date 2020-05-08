from blog_db import BlogPost


def build_db_path(directory):
    """
    Given a directory as a Path object, construct a path to a file named
    test.sqlite within that directory.
    :param directory: a Path object representing the directory
    :return: a Path object representing the path to the file
    """

    return directory / 'test.sqlite'


def test_initializer(tmp_path):
    """
    Test that the BlogPost initializer runs without errors.

    :param tmp_path: a Path object representing the path to the temporary
     directory created via the pytest tmp_path fixture
    """
    BlogPost(build_db_path(tmp_path))


def test_sign_up_entry(tmp_path):
    """
    Test that the sign_up_entry runs without raising exceptions,and correctly
    returns author that just signed up.
    This also tests the private methods insert_author and insert password
    that's used inside sign_up_entry function.
    Otherwise returns False.

    :param tmp_path: a Path object representing the path to the temporary
     directory created via the pytest tmp_path fixture
    """
    db = BlogPost(build_db_path(tmp_path))
    author_1 = db.sign_up_entry('X Æ A-12', 'password')
    assert author_1['name'] == 'X Æ A-12'
    assert author_1['name'] == db.get_author_by_name('X Æ A-12')['name']

    author_2 = db.sign_up_entry('Khandokar', 'enter')
    assert author_2 == db.get_author_by_name('Khandokar')
    assert db.sign_up_entry('Khandokar', 'override_password') is False


def test_get_author_by_name(tmp_path):
    """
    Test that the get_author_by_name runs without raising exceptions,and
    correctly returns a dictionary representing the expected author.
    Otherwise returns False.

    :param tmp_path: a Path object representing the path to the temporary
     directory created via the pytest tmp_path fixture
    """
    db = BlogPost(build_db_path(tmp_path))

    author = db.sign_up_entry('Abrar', 'umbrella')
    assert author == db.get_author_by_name('Abrar')

    author_2 = db.sign_up_entry('X Æ A-12', '13')
    assert author_2['name'] == db.get_author_by_name('X Æ A-12')['name']
    assert author_2['name'] == 'X Æ A-12'

    value = db.get_author_by_name('nonexisting')
    assert value is False


def test_get_author_by_id(tmp_path):
    """
    Test that the get_author_by_id runs without raising exceptions,and correctly
    returns a dictionary representing the expected author.
    Otherwise returns False.

    :param tmp_path: a Path object representing the path to the temporary
     directory created via the pytest tmp_path fixture
    """
    db = BlogPost(build_db_path(tmp_path))

    author = db.sign_up_entry('Abrar', 'something')
    assert author == db.get_author_by_id(1)

    author_2 = db.sign_up_entry('X Æ A-12', 'else')
    assert author_2['author_id'] == 2

    value = db.get_author_by_id('invalidtype')
    value_2 = db.get_author_by_id(3)
    assert value is False
    assert value_2 is False


def test_password_check(tmp_path):
    """
    Test that the password_check runs without raising exceptions,and correctly
    returns True if password inserted successfully.
    Otherwise returns False.

    :param tmp_path: a Path object representing the path to the temporary
     directory created via the pytest tmp_path fixture
    """
    db = BlogPost(build_db_path(tmp_path))

    assert db.sign_up_entry('Khandokar', 'password')

    assert db.password_check('Khandokar', 'password')

    assert db.password_check('Khandokar', 'wrong_password') is False

    assert db.password_check('non_existent_user', 'password') is False


def test_update_password(tmp_path):
    """
    Test that the update_password runs without raising exceptions,and correctly
    returns True if password updated successfully.
    Otherwise returns False.

    :param tmp_path: a Path object representing the path to the temporary
     directory created via the pytest tmp_path fixture
    """
    db = BlogPost(build_db_path(tmp_path))
    assert db.sign_up_entry('Khandokar', 'old_password')
    assert db.password_check('Khandokar', 'old_password')

    assert db.update_password('Khandokar', 'old_password', 'new_password')
    assert db.password_check('Khandokar', 'new_password')
    assert db.password_check('Khandokar', 'old_password') is False

    assert db.update_password('non_existent', 'password', 'update') is False


def test_insert_blog(tmp_path):
    """
    Test that insert_blog() runs without raising exceptions, and correctly
    returns a dictionary representing the new blog.
    Otherwise returns False

    :param tmp_path: a Path object representing the path to the temporary
     directory created via the pytest tmp_path fixture
    """
    db = BlogPost(build_db_path(tmp_path))

    assert db.sign_up_entry('Giraffe', 'animal')
    blog = db.insert_blog('stitle', 'ssubtitle', 'Giraffe', 'scontent')

    assert blog['title'] == 'stitle'
    assert blog['subtitle'] == 'ssubtitle'
    assert blog['author_id'] == db.get_author_by_name('Giraffe')['author_id']
    assert blog['content'] == 'scontent'
    assert db.insert_blog('title_2', 'subtitle_2', 'Giraffe', 'new_content')

    assert db.insert_blog('title', 'sub', 'fake_user', 'content') is False


def test_get_blog_by_id(tmp_path):
    """
    Test that get_blog_by_id() returns False when it should, and properly
    returns a blog when there are 1 or 2 blogs in the database.
    """

    db = BlogPost(build_db_path(tmp_path))

    assert db.get_blog_by_id(1) is False
    assert db.insert_blog('title', 'Sub', 'non_existent', 'content') is False

    assert db.sign_up_entry('KHANDOKAR', 'PASSWORD')

    blog_inserted = db.insert_blog('STITLE', 'SSUBTITLE', 'KHANDOKAR',
                                   'SCONTENT')
    blog = db.get_blog_by_id(1)

    assert blog_inserted == blog

    assert db.get_blog_by_id(23) is False

    blog_inserted = db.insert_blog('title2', 'subtitle2', 'Khandokar2',
                                   'content2')
    blog = db.get_blog_by_id(2)

    assert blog_inserted == blog


def test_get_all_posts(tmp_path):
    """
    Test that get_all_posts() properly returns an empty list when no blogs
    have been inserted, and returns a correct list of blogs when there are one
    or two blogs in the database.
    """

    db = BlogPost(build_db_path(tmp_path))

    assert db.get_all_posts() == []
    assert db.sign_up_entry('KHANDOKAR', 'PASSWORD')
    blog_1 = db.insert_blog('STITLE', 'SSUBTITLE', 'KHANDOKAR',
                                   'SCONTENT')

    assert blog_1['title'] == 'STITLE'
    assert blog_1['subtitle'] == 'SSUBTITLE'
    assert blog_1['content'] == 'SCONTENT'
    assert blog_1['author_id'] == db.get_author_by_name('KHANDOKAR')[
        'author_id']

    blogs = db.get_all_posts()

    assert len(blogs) == 1

    assert db.insert_blog('title', 'Sub', 'non_existent', 'content') is False

    assert db.sign_up_entry('khan', 'haunter')
    assert db.insert_blog('title', 'sub', 'khan', 'content')

    blogs = db.get_all_posts()
    assert len(blogs) == 2
