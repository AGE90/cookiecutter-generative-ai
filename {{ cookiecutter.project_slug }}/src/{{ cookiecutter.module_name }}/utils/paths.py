"""
Project-relative path helpers.

The project root is found with `pyprojroot.here()` (it looks for `.git/`,
`pyproject.toml`, etc.), so paths resolve the same way from scripts, notebooks
and tests, wherever they run from.

Each helper takes optional extra path parts:

>>> data_dir("docs.jsonl")  # <project root>/data/docs.jsonl
"""

from collections.abc import Callable
from pathlib import Path

from pyprojroot import here


def make_dir_function(*parts: str) -> Callable[..., Path]:
    """
    Build a function returning paths under `<project root>/<parts>`.

    Parameters
    ----------
    *parts : str
        Subdirectories of the project root, e.g. `"reports", "figures"`.

    Returns
    -------
    Callable[..., Path]
        Function that joins any extra arguments onto that directory.
    """

    def dir_path(*args: str) -> Path:
        return here().joinpath(*parts, *args)

    return dir_path


project_dir = make_dir_function()
config_dir = make_dir_function("config")
data_dir = make_dir_function("data")
docs_dir = make_dir_function("docs")
examples_dir = make_dir_function("examples")
logs_dir = make_dir_function("logs")
notebooks_dir = make_dir_function("notebooks")
references_dir = make_dir_function("references")
reports_dir = make_dir_function("reports")
reports_figures_dir = make_dir_function("reports", "figures")
tests_dir = make_dir_function("tests")
