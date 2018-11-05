import os
import re
from types import GeneratorType
from unittest import TestCase, main
from unittest.mock import patch, MagicMock

from grep import Validator, Searcher, BASE_DIR, ValidationError


def create_test_file(body: str = None):
    path = os.path.join(BASE_DIR, 'test.txt')

    if not body:
        body = 'This is test line\n'

    with open(path, 'w+') as f:
        f.write(body)

    return path


class TestValidator(TestCase):

    def setUp(self):
        self.filepath = create_test_file()

    def test_valid_path(self):
        validator = Validator(self.filepath)
        result = validator.validate_path()

        self.assertIsNone(result)
        self.assertEqual(self.filepath, validator.filepath)

    def test_non_file(self):
        validator = Validator(BASE_DIR)

        with self.assertRaises(ValidationError):
            validator.validate_path()

    def test_wrong_mimetype(self):
        path = os.path.join(BASE_DIR, __file__)

        validator = Validator(path)

        with self.assertRaises(ValidationError):
            validator.validate_path()

    def tearDown(self):
        os.remove(self.filepath)


class TestSearcher(TestCase):

    def setUp(self):
        self.content = 'This is maybe some text'
        self.filepath = create_test_file(self.content)

    @patch('grep.Searcher._search')
    def test_find(self, search_mock: MagicMock):
        search_mock.return_value = self.content

        text = 'This'
        searcher = Searcher(text, self.filepath)

        gen = searcher.find()
        self.assertIsNotNone(gen)
        self.assertIsInstance(gen, GeneratorType)

        result = next(gen)
        self.assertIsNotNone(result)
        self.assertEqual(result, self.content)

    @patch('grep.Searcher._search')
    def test_find_not_included(self, search_mock: MagicMock):
        search_mock.return_value = None

        text = 'asdasdasdasd'
        searcher = Searcher(text, self.filepath)

        gen = searcher.find(True)
        self.assertIsNotNone(gen)
        self.assertIsInstance(gen, GeneratorType)

        result = next(gen)
        self.assertIsNotNone(result)
        self.assertEqual(result, self.content)

    def test_find_wrong_path(self):
        path = 'asdasdsadsas'

        text = 'test'
        searcher = Searcher(text, path)
        gen = searcher.find()

        with self.assertRaises(FileNotFoundError):
            next(gen)

    def test_search(self):
        text = 'This'

        searcher = Searcher(text, self.filepath)
        result = searcher._search(self.content)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, re.Match)

        self.assertEqual(result.group(0), text)

    def test_wrong_search(self):
        text = 'asdasdasd'

        searcher = Searcher(text, self.filepath)
        result = searcher._search(self.content)

        self.assertIsNone(result)

    def tearDown(self):
        os.remove(self.filepath)


if __name__ == '__main__':
    main()
