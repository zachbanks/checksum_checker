import pytest
from src.hasher import Hasher

class TestHasher:
    def test_init(self):
        hasher = Hasher("1234")
        assert hasher.hash == "1234"
        assert hasher.algorithm != None


    def test_str(self):
        h = Hasher("1234")
        assert str(h) == "1234"


    def test_eq(self):
        h1 = Hasher("1234")
        h2 = Hasher("1234")
        h3= Hasher("12345")

        assert h1 == h2
        assert h1 != h3

    
    # TODO: Implement
    def test_genenerate_from_file(self):
        # Test raises exception if bad algo given.
        # Test raises exception if bad file given.
        # Test no errors given correct algos (whole list)
        # Test generates correct checksum for given file.
        # Tests returns checksum for given file.