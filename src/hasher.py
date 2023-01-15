import hashlib
import pathlib
from dataclasses import dataclass
from typing import Union, Self


@dataclass
class Hasher:
    DEFAULT_ALGORITHM = "sha256"
    ALGORITHMS = hashlib.algorithms_guaranteed
    hash: str
    algorithm: str = DEFAULT_ALGORITHM

    @classmethod
    def generate_hash_from_file(
        cls, file_path: Union[str, pathlib.Path], algorithm: str = DEFAULT_ALGORITHM
    ) -> str:
        """
        Generates a hash given the algorithm and file path.
        """
        if not algorithm in cls.ALGORITHMS:
            raise ValueError(f"Must use supported hash algorithm: {cls.ALGORITHMS}")

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
            raise ValueError(f"Must use supported hash algorithm: {cls.ALGORITHMS}")

        return hasher

    def __eq__(self, obj: Self) -> bool:
        """
        Compares two hashes and returns if they are equal or not.
        """
        return self.hash == obj.hash

    def __str__(self) -> str:
        return self.hash
