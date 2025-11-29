#!/usr/bin/env python3
"""
hooks/post_gen_project.py

Safe post-generation hook for cookiecutter-generative-ai.

This script purposely avoids third-party runtime dependencies so it can run
inside the environment cookiecutter uses to render hooks. It writes files as
plain text (TOML/YAML) and prints next steps rather than performing network
operations by default.
"""
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List

# --- Cookiecutter variables ---
PROJECT_NAME = "{{ cookiecutter.project_name }}"
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
MODULE_NAME = "{{ cookiecutter.module_name }}"
PROJECT_SHORT_DESCRIPTION = "{{ cookiecutter.project_short_description }}"
AUTHOR_NAME = "{{ cookiecutter.author_name }}"
AUTHOR_EMAIL = "{{ cookiecutter.author_email }}"
PROJECT_VERSION = "{{ cookiecutter.project_version }}"
PROJECT_URL = "{{ cookiecutter.project_url }}"
PYTHON_VERSION = "{{ cookiecutter.python_version }}"
LICENSE = "{{ cookiecutter.license }}"
PACKAGE_MANAGER = "{{ cookiecutter.package_manager }}"
PROJECT_DEPENDENCIES = "{{ cookiecutter.project_dependencies }}"
DEV_DEPENDENCIES = "{{ cookiecutter.dev_dependencies }}"
TESTING_DEPENDENCIES = "{{ cookiecutter.testing_dependencies }}"
INITIALIZE_GIT_REPOSITORY = "{{ cookiecutter.initialize_git_repository }}" == "yes"


# Parse dependency comma-separated strings into lists
def _split_deps(raw: str) -> List[str]:
    if not raw:
        return []
    return [d.strip() for d in raw.split(",") if d.strip()]


PROJECT_DEPS = _split_deps(PROJECT_DEPENDENCIES)
DEV_DEPS = _split_deps(DEV_DEPENDENCIES)
TESTING_DEPS = _split_deps(TESTING_DEPENDENCIES)


def run(cmd: List[str], check: bool = True, **kwargs) -> subprocess.CompletedProcess:
    """Run a shell command and return the CompletedProcess.

    This helper prints the command and runs it. It is used only for local
    operations like initializing git. The hook avoids network operations by
    default.
    """
    print(f"Running: {' '.join(cmd)}")
    try:
        return subprocess.run(cmd, check=check, **kwargs)
    except subprocess.CalledProcessError:
        print(f"Command failed: {' '.join(cmd)}")
        raise


def setup_uv() -> None:
    """Initialize uv project."""
    # Check if uv is installed
    if not shutil.which("uv"):
        print("ERROR: 'uv' is not installed or not in PATH.")
        print("Install 'uv' to manage your project dependencies.")
        sys.exit(1)

    # Initialize uv project
    run(["uv", "init"])

    # Add main dependencies
    if PROJECT_DEPS:
        run(["uv", "add"] + PROJECT_DEPS)

    # Add dev and test dependencies
    if DEV_DEPS:
        run(["uv", "add", "--dev"] + DEV_DEPS)

    # Add testing dependencies
    if TESTING_DEPS:
        run(["uv", "add", "--dev"] + TESTING_DEPS)


def setup_poetry() -> None:
    """Initialize Poetry project."""
    # Check if poetry is installed
    if not shutil.which("poetry"):
        print("ERROR: 'poetry' is not installed or not in PATH.")
        print("Install 'poetry' to manage your project dependencies.")
        sys.exit(1)

    # Create virtual environments within the project directory
    run(["poetry", "config", "virtualenvs.in-project", "true", "--local"])

    # Initialize poetry project
    run(
        [
            "poetry", "init",
            "--name", PROJECT_SLUG,
            "--description", PROJECT_SHORT_DESCRIPTION,
            "--author", f"{AUTHOR_NAME} <{AUTHOR_EMAIL}>",
            "--python", f"^{PYTHON_VERSION}",
            "--no-interaction",
        ]
    )

    # Install the project
    run(["poetry", "install"])

    # Add main dependencies
    if PROJECT_DEPS:
        run(["poetry", "add"] + PROJECT_DEPS)

    # Add dev dependencies
    if DEV_DEPS:
        run(["poetry", "add", "--group", "dev"] + DEV_DEPS)

    # Add testing dependencies
    if TESTING_DEPS:
        run(["poetry", "add", "--group", "test"] + TESTING_DEPS)


def setup_pip_tools() -> None:
    """Initialize pip-tools project by creating .in files and compiling them."""
    # Check if pip-compile is installed
    if not shutil.which("pip-compile"):
        print("ERROR: 'pip-tools' is not installed or not in PATH.")
        print("Install 'pip-tools' to manage your project dependencies.")
        sys.exit(1)

    print("\nSetting up pip-tools configuration...")

    # Write requirements.in (production dependencies)
    requirements_lines = []
    if PROJECT_DEPS:
        requirements_lines.append("# Production dependencies")
        requirements_lines.extend(PROJECT_DEPS)
    else:
        requirements_lines.append("# Add your production dependencies here")

    Path("requirements.in").write_text(
        "\n".join(requirements_lines) + "\n", encoding="utf-8")
    print("✓ Created requirements.in")

    # Write requirements-dev.in (development dependencies)
    dev_lines = [
        "# Development dependencies",
        "-r requirements.in  # Include production dependencies",
        ""
    ]

    if DEV_DEPS:
        dev_lines.append("# Development tools")
        dev_lines.extend(DEV_DEPS)
        dev_lines.append("")

    if TESTING_DEPS:
        dev_lines.append("# Testing dependencies")
        dev_lines.extend(TESTING_DEPS)
        dev_lines.append("")

    Path("requirements-dev.in").write_text("\n".join(dev_lines), encoding="utf-8")
    print("✓ Created requirements-dev.in")

    # Compile requirements files
    print("\nCompiling requirements files...")
    run(["pip-compile", "requirements.in", "--output-file", "requirements.txt"])
    print("✓ Compiled requirements.txt")

    run(["pip-compile", "requirements-dev.in",
        "--output-file", "requirements-dev.txt"])
    print("✓ Compiled requirements-dev.txt")

    # Install dependencies
    print("\nInstalling dependencies...")
    run([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"])
    print("✓ Dependencies installed")

    print("\npip-tools setup complete!")
    print("Next steps:")
    print("  pip-compile --upgrade requirements.in     # Update dependencies")
    print("  pip-sync requirements-dev.txt             # Sync environment exactly")


def setup_pip() -> None:
    """Initialize pip project by creating requirements.txt."""
    print("\nSetting up pip configuration...")

    # Write requirements.txt (production dependencies)
    requirements_lines = []
    if PROJECT_DEPS:
        requirements_lines.append("# Production dependencies")
        requirements_lines.extend(PROJECT_DEPS)
    else:
        requirements_lines.append("# Add your production dependencies here")

    if DEV_DEPS or TESTING_DEPS:
        requirements_lines.append("\n# Development and Testing dependencies")
        requirements_lines.extend(DEV_DEPS)
        requirements_lines.extend(TESTING_DEPS)

    Path("requirements.txt").write_text(
        "\n".join(requirements_lines) + "\n", encoding="utf-8")
    print("✓ Created requirements.txt")

    # Install dependencies
    print("\nInstalling dependencies...")
    run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✓ Dependencies installed")

    print("\npip setup complete!")
    print("Next steps:")
    print("  pip install -r requirements.txt           # Install dependencies")

def setup_git() -> None:
    """Initialize a git repository and do an initial commit if requested."""

    print("\nInitializing git repository...")
    run(["git", "init"])
    run(["git", "add", "."])
    run(["git", "commit", "-m", "Initial commit"])


def main() -> None:
    """Main entry point for the post-generation hook."""
    try:
        if PACKAGE_MANAGER == "uv":
            setup_uv()
        elif PACKAGE_MANAGER == "poetry":
            setup_poetry()
        elif PACKAGE_MANAGER == "pip-tools":
            setup_pip_tools()

        if INITIALIZE_GIT_REPOSITORY:
            setup_git()

        print("\n=== Project setup complete ===")
        print(
            f"Project '{PROJECT_NAME}' created")
    except (subprocess.CalledProcessError, FileNotFoundError, OSError) as exc:  # pragma: no cover - run-time safety
        print(f"Error during post-generation hook: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
