import re
import argparse


def main():
    parser = argparse.ArgumentParser(description='Grep utility on Python')
    parser.add_argument('search', help='Text to find in file. Can be a regex.')
    parser.add_argument('filepath', help='Path to file')
    parser.add_argument('-v', action='store_true')
    args = parser.parse_args()

    search = args.search
    filepath = args.filepath
    not_included = args.v

    searcher = Searcher(search, filepath)
    for line in searcher.find(not_included):
        if line:
            print(line)


class Searcher:

    def __init__(self, search: str, filepath: str):
        self.search = re.compile(search)
        self.file = filepath

    def find(self, not_include: bool = False):
        with open(self.file, 'r') as f:
            for line in f:
                result = self._processing(line)

                if (result is None and not_include) or result is not None:
                    yield line

    def _processing(self, line: str):
        return self.search.search(line)


if __name__ == '__main__':
    main()
