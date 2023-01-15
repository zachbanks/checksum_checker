import hashlib
import pathlib
import pytest
from termcolor import colored
from typing import Union, Self, Optional
from dataclasses import dataclass
import pyperclip
import typer

# TODO: Switch color output to use Rich
# from rich import print


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


def main(
    test: str = typer.Argument(
        ...,
        help="Provide file path of file to check against source.",
        show_default=False,
        metavar="Test File",
    ),
    source: str = typer.Argument(
        pyperclip.paste(),
        help="Provide source SHA to test against test file. If not provided, will use system clipboard contents.",
        show_default="System clipboard contents",
        metavar="Source Hash",
    ),
    algorithm: str = typer.Option(
        Hasher.DEFAULT_ALGORITHM,
        "--algorithm",
        "-a",
        help=f"Choose hash algorithm to use: {Hasher.ALGORITHMS}",
    ),
) -> None:
    """
    Generates hash value for a specified file and compares it against a known value.
    Used to verify if software downloaded from internet has been maliciously modified
    or is not from the original source.
    """

    source = Hasher(hash=source, algorithm=algorithm)
    test = Hasher.generate_hash_from_file(test, algorithm=algorithm)

    # Colorize output and print to terminal
    result = source == test
    color = "green" if result else "red"

    result: str = str(result).upper()
    colored_result = colored(result, "black", f"on_{color}", attrs=["bold"])

    output = colored(f"[{algorithm}] {source} == {test}: ", color) + colored_result

    print(output)


if __name__ == "__main__":
    typer.run(main)
