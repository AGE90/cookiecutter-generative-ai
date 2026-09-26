"""
Render the template without the network-dependent hooks and check the output.

Run with: uvx --with cookiecutter pytest tests/
"""

import tomllib
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter

TEMPLATE_DIR = Path(__file__).resolve().parents[1]
OFFLINE = {"initialize_env": "no", "initialize_git_repository": "no"}


def render(tmp_path, **context):
    """Generate a project into tmp_path and return its path."""
    out = cookiecutter(
        str(TEMPLATE_DIR),
        no_input=True,
        output_dir=str(tmp_path),
        extra_context={**OFFLINE, "project_name": "Demo Agent", **context},
    )
    return Path(out)


@pytest.mark.parametrize("license_", ["MIT", "Apache-2.0", "No license file"])
def test_render(tmp_path, license_):
    project = render(tmp_path, license=license_, python_version="3.13")

    assert project.name == "demo-agent"
    for rel in [
        "pyproject.toml",
        "Makefile",
        "CLAUDE.md",
        ".env",
        ".env.example",
        "src/demo_agent/graph.py",
        "tests/conftest.py",
    ]:
        assert (project / rel).is_file(), rel
    assert (project / "LICENSE").exists() == (license_ != "No license file")

    pyproject = tomllib.loads((project / "pyproject.toml").read_text())
    assert pyproject["project"]["name"] == "demo_agent"
    assert pyproject["project"]["requires-python"] == ">=3.13"
    assert pyproject["project"].get("license") == (
        None if license_ == "No license file" else license_
    )
    assert pyproject["project"]["scripts"] == {"demo-agent": "demo_agent.__main__:main"}
    assert pyproject["tool"]["ruff"]["target-version"] == "py313"

    leftovers = [
        p for p in project.rglob("*")
        if p.is_file() and ("{{" in p.read_text(errors="ignore") or "{%" in p.read_text(errors="ignore"))
    ]
    assert not leftovers, leftovers


@pytest.mark.parametrize(
    ("provider", "model", "key_var"),
    [
        ("anthropic", "anthropic:claude-opus-5", "ANTHROPIC_API_KEY"),
        ("openai", "openai:gpt-5", "OPENAI_API_KEY"),
        ("ollama", "ollama:llama3.2", None),
    ],
)
def test_llm_provider(tmp_path, provider, model, key_var):
    project = render(tmp_path, llm_provider=provider)

    env = (project / ".env.example").read_text()
    assert f"LLM_MODEL={model}" in env
    config = (project / "src/demo_agent/config.py").read_text()
    assert f'"{model}"' in config
    if key_var:
        assert f"{key_var}=" in env
    else:
        assert "API_KEY" not in env and "ollama pull llama3.2" in env


@pytest.mark.parametrize(
    "bad", [{"author_email": "not-an-email"}, {"python_version": "3.10"}, {"python_version": "3.12.1"}]
)
def test_invalid_input_fails(tmp_path, bad):
    with pytest.raises(Exception):
        render(tmp_path, **bad)
