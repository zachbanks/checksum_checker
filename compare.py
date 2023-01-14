#! venv/python
import hashlib
import argparse
import pathlib
import pytest
from typing import Union


def generate_hash(
    file_path: Union[str, pathlib.Path], algorithm: str = "sha256"
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

    if hasattr(hashlib, algorithm):
        func = getattr(hashlib, algorithm)
        result = func(contents)
    else:
        raise ValueError(f"Must use supported hash algorithm: {ALGORITHMS}")

    return result.hexdigest()


def sha_compare(original: str, test: str) -> bool:
    """
    Compares two shas and returns if they are equal or not.
    """
    return original == test


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
    parser.add_argument("--sha256", dest="sha256", default=True)
    parser.add_argument("source", help="Source SHA")
    parser.add_argument("test", help="Test SHA")
    args = parser.parse_args()

    source: str = args.source
    test: str = args.test
    result: bool = sha_compare(source, test)

    print(f"Comparing '{source}' to '{test}': {str(result).upper()}")


if __name__ == "__main__":
    # main()
    print(generate_hash("~/Desktop/path.txt", "sha256"))
