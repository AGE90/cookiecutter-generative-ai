#!/usr/bin/env python3
"""
Post-generation hook for cookiecutter-generative-ai.

1. License: removes the empty LICENSE file when "No license file" was selected
2. uv environment: pins Python and adds each dependency group with `uv add`
3. .env: creates it from .env.example
4. Git: initializes a repository and makes the initial commit

Uses only the standard library, so it runs in the environment cookiecutter uses.
"""

import shutil
import subprocess
import sys
from pathlib import Path

# Keep our messages in order with subprocess output when stdout is piped
sys.stdout.reconfigure(line_buffering=True)

# Colored output with plain ANSI codes
MSG_COLOR = "\033[36m"
ERROR_COLOR = "\033[31m"
RESET = "\033[0m"

# --- Cookiecutter variables ---
LICENSE = "{{ cookiecutter.license }}"
PYTHON_VERSION = "{{ cookiecutter.python_version }}"
INITIALIZE_ENV = "{{ cookiecutter.initialize_env }}" == "yes"
INITIALIZE_GIT_REPOSITORY = "{{ cookiecutter.initialize_git_repository }}" == "yes"
LLM_PACKAGE = "{{ cookiecutter._llm_packages[cookiecutter.llm_provider] }}"

PROJECT_DEPENDENCIES = "{{ cookiecutter.project_dependencies }}"
EXTRA_DEPENDENCIES = "{{ cookiecutter.extra_dependencies }}"
DEV_DEPENDENCIES = "{{ cookiecutter.development_dependencies }}"
TEST_DEPENDENCIES = "{{ cookiecutter.testing_dependencies }}"


def info(msg: str) -> None:
    """Print an informational message."""
    print(f"{MSG_COLOR}{msg}{RESET}")


def run(cmd: list[str]) -> None:
    """
    Run a command and exit with an error message if it fails.

    Parameters
    ----------
    cmd : list of str
        Command and arguments to execute.
    """
    try:
        subprocess.check_call(cmd)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"{ERROR_COLOR}Command failed: {' '.join(cmd)}\n{exc}{RESET}")
        sys.exit(1)


def split_deps(raw: str) -> list[str]:
    """Turn a comma-separated dependency string into a list of packages."""
    return [dep.strip() for dep in raw.split(",") if dep.strip()]


def remove_license() -> None:
    """Remove the empty LICENSE file when no license was selected."""
    if LICENSE == "No license file":
        Path("LICENSE").unlink(missing_ok=True)


def setup_env() -> None:
    """Pin Python and add every dependency group with uv."""
    if not shutil.which("uv"):
        print(f"{ERROR_COLOR}'uv' is not installed: https://docs.astral.sh/uv/{RESET}")
        sys.exit(1)

    info(f"Pinning Python {PYTHON_VERSION}...")
    run(["uv", "python", "pin", PYTHON_VERSION])

    groups = [
        (PROJECT_DEPENDENCIES + "," + LLM_PACKAGE + "," + EXTRA_DEPENDENCIES, []),
        (DEV_DEPENDENCIES, ["--group", "dev"]),
        (TEST_DEPENDENCIES, ["--group", "test"]),
    ]
    for raw, group_args in groups:
        pkgs = split_deps(raw)
        if pkgs:
            info(f"Adding dependencies: {', '.join(pkgs)} {' '.join(group_args)}")
            run(["uv", "add", *group_args, *pkgs])


def create_env_file() -> None:
    """Create .env from .env.example if it doesn't exist yet."""
    if not Path(".env").exists():
        shutil.copy(".env.example", ".env")
        info("Created .env from .env.example. Add your API key there.")


def setup_git() -> None:
    """Initialize a git repository and make the initial commit."""
    info("Initializing Git repository...")
    run(["git", "init"])
    run(["git", "add", "."])
    run(["git", "commit", "-m", "Initial commit"])


def main() -> None:
    """Run the post-generation tasks selected by the user."""
    remove_license()
    create_env_file()

    if INITIALIZE_ENV:
        setup_env()
    else:
        info("Skipping uv environment setup. Run `make install` later.")

    if INITIALIZE_GIT_REPOSITORY:
        setup_git()

    info("All post-generation tasks completed!")


if __name__ == "__main__":
    main()
