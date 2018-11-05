import os.path
import re
import argparse
import mimetypes
from typing import Generator, Optional

# Base directory path
BASE_DIR = os.path.dirname(__file__)
# Allowed file mimetype
FILE_MIMETYPE = 'text/plain'


class GrepException(Exception):
    pass


class ValidationError(GrepException):
    pass


class Validator:
    """Class for validate input data."""

    def __init__(self, filepath: str):
        """Constructor.

        Args:
            filepath (str): full path to file.
        """
        self.filepath = filepath

    def validate_path(self):
        """Check if file exist and have the right mimetype.

        Raises:
            :py:obj:`ValidationError`: Error if file is not exist or haven't
                wrong mimetype.
        """
        if not os.path.isfile(self.filepath):
            raise ValidationError(f'{self.filepath} is not a file.')

        mimetype, _ = mimetypes.guess_type(self.filepath)
        if mimetype is None or mimetype != FILE_MIMETYPE:
            msg = f'{self.filepath} has wrong mimetype {mimetype}. '\
                f'File must be a {FILE_MIMETYPE} type.'
            raise ValidationError(msg)


class Searcher:
    """Class for search text in a file by it's path."""

    def __init__(self, text: str, filepath: str):
        """Constructor.

        Args:
            text (str): text to search. Can be a regex expression.
            filepath (str): full path to file.
        """
        self.text = re.compile(text)
        self.file = filepath

    def find(self, not_include: bool = False) -> Generator[str, None, None]:
        """Find a line in a file.

        Args:
            not_include (bool): If True find a line that not contain a string.

        Returns:
            generator: return a search line.
        """
        with open(self.file, 'r') as f:
            for line in f:
                result = self._search(line)

                if (result is None and not_include) or result is not None:
                    yield line

    def _search(self, line: str) -> re.Match:
        """Search a precompilated string in a text line.

        Args:
            line (str): line to search.

        Returns:
            re.Match: a corresponding match object.
        """
        return self.text.search(line)


def main():
    parser = argparse.ArgumentParser(description='Grep utility on Python')
    parser.add_argument('text', help='Text to find in file. Can be a regex.')
    parser.add_argument('filepath', help='Path to file')
    parser.add_argument('-v', action='store_true',
                        help='Print lines which do not contain a text')
    args = parser.parse_args()

    text = args.text
    filepath = os.path.join(BASE_DIR, args.filepath)
    not_included = args.v

    validator = Validator(filepath)
    validator.validate_path()

    searcher = Searcher(text, filepath)
    for line in searcher.find(not_included):
        if line:
            print(line)


if __name__ == '__main__':
    main()
