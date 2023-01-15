#!venv/bin/python

import hashlib
import argparse
import pathlib
import pytest
from termcolor import colored
from typing import Union, Self
from dataclasses import dataclass


@dataclass
class Hasher:
    DEFAULT_ALGORITHM = "sha256"
    hash: str
    algorithm: str = DEFAULT_ALGORITHM

    @classmethod
    def generate_hash_from_file(
        cls, file_path: Union[str, pathlib.Path], algorithm: str = DEFAULT_ALGORITHM
    ) -> str:
        """
        Generates a hash given the algorithm and file path.
        """
        ALGORITHMS = hashlib.algorithms_guaranteed
        if not algorithm in ALGORITHMS:
            raise ValueError(f"Must use supported hash algorithm: {ALGORITHMS}")

        # Read file contents
        try:
            with open(pathlib.Path(file_path).expanduser(), "rb") as file:
                contents = file.read()
        except FileNotFoundError as exception:
            print(f"File not found: {file_path}")
            raise

        # Dynamically call hash algo given argument name.
        if hasattr(hashlib, algorithm):
            func = getattr(hashlib, algorithm)
            result = func(contents).hexdigest()
            hasher = cls(hash=result, algorithm=algorithm)
        else:
            raise ValueError(f"Must use supported hash algorithm: {ALGORITHMS}")

        return hasher

    def __eq__(self, obj: Self) -> bool:
        """
        Compares two hashes and returns if they are equal or not.
        """
        return self.hash == obj.hash

    def __str__(self) -> str:
        return self.hash


# TODO: Update tests
def test_sha_compare():
    original: str = ""
    test: str = ""
    assert sha_compare(original, test) == True

    test = "x"
    assert sha_compare(original, test) == False


def test_generate_hash():
    # TODO: Figure out how to test this.
    path = "somefilepath.txt"
    assert generate_hash(path, "sha256")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare two SHAs to see if they are equal."
    )
    parser.add_argument("-a", dest="algorithm", default=Hasher.DEFAULT_ALGORITHM)
    parser.add_argument("source", help="Source SHA")
    parser.add_argument("test", help="Test SHA")
    args = parser.parse_args()

    algorithm = args.algorithm
    source = Hasher(hash=args.source, algorithm=algorithm)
    test = Hasher.generate_hash_from_file(args.test, algorithm=algorithm)

    # Colorize output and print to terminal
    result = source == test
    color = "green" if result else "red"

    result: str = str(result).upper()
    colored_result = colored(result, "black", f"on_{color}", attrs=["bold"])

    output = colored(f"[{algorithm}] {source} == {test}: ", color) + colored_result

    print(output)


if __name__ == "__main__":
    main()
