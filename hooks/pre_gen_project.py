#!/usr/bin/env python3
"""
Pre-generation validation for Cookiecutter templates.

Validates:
- `module_name` is a valid Python identifier and not a keyword.
- `project_slug` is a lower-case hyphen-separated slug.
- `author_email` (only if provided) matches a simple email pattern.
- `project_url` (only if provided) looks like a URL (has scheme+netloc).
- `python_version` (only if provided) matches "3.x" or "3.x.y" and meets a minimum (default 3.9).
"""

import keyword
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

# Try optional colored output (do not require colorama)
try:
    from colorama import Fore, Style, just_fix_windows_console # type: ignore

    just_fix_windows_console()
    ERR = Fore.RED
    INFO = Fore.CYAN
    RESET = Style.RESET_ALL
except ImportError:
    ERR = INFO = RESET = ""

# Cookiecutter variables (filled by cookiecutter)
PROJECT_NAME = "{{ cookiecutter.project_name }}"
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
MODULE_NAME = "{{ cookiecutter.module_name }}"
AUTHOR_EMAIL = "{{ cookiecutter.author_email }}"
PROJECT_URL = "{{ cookiecutter.project_url }}"
PYTHON_VERSION = "{{ cookiecutter.python_version }}"

# Validation patterns
MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]*$"
SLUG_REGEX = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
EMAIL_REGEX = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
PYTHON_REGEX = r"^3\.\d+(\.\d+)?$"

MIN_PYTHON_MINOR = 9  # require at least 3.9; change to 10 if you prefer 3.10+


def die(msg: str) -> None:
    """Abort execution with an error message.

    Parameters
    ----------
    msg : str
        The error message to display.
    """
    print(f"{ERR}ERROR: {msg}{RESET}")
    sys.exit(1)


def info(msg: str) -> None:
    """Display an informational message.

    Parameters
    ----------
    msg : str
        The informational message to display.
    """
    print(f"{INFO}{msg}{RESET}")


def validate_module(name: str) -> None:
    """Validate that the module name is a valid Python identifier and not a keyword.

    Parameters
    ----------
    name : str
        The module name to validate.
    """
    if not name:
        die("`module_name` is empty. Provide a valid Python package name.")
    if not re.match(MODULE_REGEX, name):
        die(
            "`module_name` must start with a letter or underscore and contain only "
            "letters, numbers, or underscores."
        )
    if keyword.iskeyword(name):
        die(f"`module_name` '{name}' is a Python reserved keyword.")
    info(f"Valid module name: {name}")


def validate_slug(slug: str) -> None:
    """Validate that the project slug is a lower-case hyphen-separated string.

    Parameters
    ----------
    slug : str
        The project slug to validate.
    """
    if not slug:
        die("`project_slug` is empty. Provide a project slug.")
    if not re.match(SLUG_REGEX, slug):
        die(
            "`project_slug` must be lower-case, alphanumeric and may contain single hyphens "
            "(e.g. my-project, not My_Project or my--project)."
        )
    info(f"Valid project slug: {slug}")


def validate_email(email: str) -> None:
    """Validate that the author email matches a simple email pattern.

    Parameters
    ----------
    email : str
        The author email to validate.
    """
    if not email or email.strip() == "":
        info("No `author_email` provided — skipping email validation.")
        return
    if not re.match(EMAIL_REGEX, email):
        die(f"Invalid `author_email` format: {email}")
    info(f"Valid author email: {email}")


def validate_url(url: str) -> None:
    """Validate that the project URL looks like a URL (has scheme and netloc).

    Parameters
    ----------
    url : str
        The project URL to validate.
    """
    if not url or url.strip() == "":
        info("No `project_url` provided — skipping URL validation.")
        return
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        die(f"Invalid `project_url`: {url}")
    info(f"Valid project URL: {url}")


def validate_python_version(version: str) -> None:
    """Validate that the Python version matches "3.x" or "3.x.y" and meets a minimum.

    Parameters
    ----------
    version : str
        The Python version to validate.
    """
    if not version or version.strip() == "":
        info("No `python_version` provided — skipping Python version validation.")
        return
    if not re.match(PYTHON_REGEX, version):
        die("`python_version` must look like '3.x' or '3.x.y' (example: '3.11').")
    parts = version.split(".")
    try:
        major = int(parts[0])
        minor = int(parts[1]) if len(parts) > 1 else 0
        if major != 3 or minor < MIN_PYTHON_MINOR:
            die(
                f"Minimum supported Python version is 3.{MIN_PYTHON_MINOR} (you provided {version}).")
        info(f"Valid Python version: {version}")
    except ValueError:
        die("`python_version` contains non-numeric components.")


def main() -> None:
    """
    Run all validations before project generation.
    """
    # Core validations
    validate_module(MODULE_NAME)
    validate_slug(PROJECT_SLUG)

    # Optional validations (only if values provided)
    validate_email(AUTHOR_EMAIL)
    validate_url(PROJECT_URL)
    validate_python_version(PYTHON_VERSION)

    # Report where the project will be created
    full_path = Path.cwd() / PROJECT_SLUG
    info(f"Project '{PROJECT_NAME}' will be created in: {full_path}")


if __name__ == "__main__":
    main()
