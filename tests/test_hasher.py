import pytest
from src.hasher import Hasher

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
