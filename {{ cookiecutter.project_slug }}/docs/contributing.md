# Contributing Guide

Thank you for your interest in contributing to {{ cookiecutter.project_name }}! This document provides guidelines and instructions for contributing.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Workflow](#development-workflow)
5. [Coding Standards](#coding-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation](#documentation)
8. [Submitting Changes](#submitting-changes)
9. [Review Process](#review-process)
10. [Community](#community)

---

## Code of Conduct

This project adheres to a [Code of Conduct](code_of_conduct.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to {{ cookiecutter.author_email }}.

---

## Getting Started

### Prerequisites

- Python {{ cookiecutter.python_version }}+
- Git
{%- if cookiecutter.package_manager == "uv" %}
- uv package manager
{%- elif cookiecutter.package_manager == "poetry" %}
- Poetry package manager
{%- endif %}

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork:**

   ```bash
   git clone {{ cookiecutter.project_url }}
   cd {{ cookiecutter.project_slug }}
   ```

3. **Add upstream remote:**

   ```bash
   git remote add upstream {{ cookiecutter.project_url }}
   ```

4. **Install dependencies:**

   ```bash
   {%- if cookiecutter.package_manager == "uv" %}
   uv sync --group dev
   {%- elif cookiecutter.package_manager == "poetry" %}
   poetry install --with dev
   {%- else %}
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements-dev.txt
   {%- endif %}
   ```

5. **Install pre-commit hooks:**

   ```bash
   {%- if cookiecutter.package_manager == "uv" %}
   uv run pre-commit install
   {%- elif cookiecutter.package_manager == "poetry" %}
   poetry run pre-commit install
   {%- else %}
   pre-commit install
   {%- endif %}
   ```

6. **Verify setup:**

   ```bash
   {%- if cookiecutter.package_manager == "uv" %}
   uv run pytest
   {%- elif cookiecutter.package_manager == "poetry" %}
   poetry run pytest
   {%- else %}
   pytest
   {%- endif %}
   ```

---

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- 🐛 **Bug fixes**: Fix issues and improve stability
- ✨ **New features**: Add new functionality
- 📚 **Documentation**: Improve or add documentation
- 🧪 **Tests**: Add or improve test coverage
- 🎨 **Code quality**: Refactoring and optimization
- 🔧 **Tooling**: Improve development tools and workflows

### Finding Something to Work On

1. **Check the issue tracker** for:
   - Issues labeled `good first issue` (great for newcomers)
   - Issues labeled `help wanted`
   - Open feature requests

2. **Read existing discussions** to understand context

3. **Ask questions** if something is unclear

### Before You Start

- **Check if an issue exists** for what you want to work on
- **Comment on the issue** to let others know you're working on it
- **Discuss major changes** before implementing them
- **Keep pull requests focused** on a single issue/feature

---

## Development Workflow

### 1. Create a Branch

Create a feature branch from `main`:

```bash
git checkout main
git pull upstream main
git checkout -b feature/your-feature-name
```

Branch naming conventions:

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation changes
- `test/description` - Test additions/changes
- `refactor/description` - Code refactoring

### 2. Make Your Changes

- Write clear, readable code
- Follow the [coding standards](#coding-standards)
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

Run the test suite:

```bash
# Run all tests
{%- if cookiecutter.package_manager == "uv" %}
uv run pytest
{%- elif cookiecutter.package_manager == "poetry" %}
poetry run pytest
{%- else %}
pytest
{%- endif %}

# Run with coverage
{%- if cookiecutter.package_manager == "uv" %}
uv run pytest --cov={{ cookiecutter.module_name }} --cov-report=term-missing
{%- elif cookiecutter.package_manager == "poetry" %}
poetry run pytest --cov={{ cookiecutter.module_name }} --cov-report=term-missing
{%- else %}
pytest --cov={{ cookiecutter.module_name }} --cov-report=term-missing
{%- endif %}
```

### 4. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: add new agent tool for web scraping

- Implement WebScraperTool class
- Add tests for web scraping functionality
- Update documentation with usage examples

Closes #123"
```

**Commit message format:**

```text
<type>: <subject>

<body>

<footer>
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `style`: Code style changes (formatting, etc.)
- `chore`: Maintenance tasks

### 5. Keep Your Branch Updated

Regularly sync with upstream:

```bash
git fetch upstream
git rebase upstream/main
```

### 6. Push Your Changes

```bash
git push origin feature/your-feature-name
```

---

## Coding Standards

### Style Guide

Follow [PEP 8](https://pep8.org/) and project-specific conventions:

- **Line length**: 100 characters max
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Use double quotes for strings
- **Naming**:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants

### Code Formatting

Format code before committing:

```bash
{%- if cookiecutter.package_manager == "uv" %}
uv run ruff format .
uv run ruff check . --fix
{%- elif cookiecutter.package_manager == "poetry" %}
poetry run ruff format .
poetry run ruff check . --fix
{%- else %}
ruff format .
ruff check . --fix
{%- endif %}
```

### Type Hints

Use type hints for all function signatures:

```python
from typing import List, Optional, Dict

def process_data(
    items: List[str],
    config: Optional[Dict[str, int]] = None
) -> List[int]:
    """Process data items."""
    ...
```

### Documentation

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int = 0) -> bool:
    """Brief description of the function.
    
    Longer description if needed, explaining the function's
    purpose and behavior in detail.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 0)
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
        
    Example:
        >>> result = example_function("test", 42)
        >>> print(result)
        True
    """
    ...
```

---

## Testing Guidelines

### Writing Tests

1. **Test file naming**: `test_*.py` or `*_test.py`
2. **Test function naming**: `test_<what_is_being_tested>`
3. **Use descriptive names**: Test name should describe what's being tested
4. **One assertion per test** (when practical)
5. **Use fixtures** for common setup

### Test Structure

```python
def test_feature_name():
    """Test description."""
    # Arrange: Set up test data
    input_data = "test"
    expected = "result"
    
    # Act: Execute the code being tested
    result = function_to_test(input_data)
    
    # Assert: Verify the results
    assert result == expected
```

### Coverage Requirements

- Aim for **>80% code coverage**
- All new features must have tests
- Bug fixes should include regression tests

### Running Tests

```bash
# Run all tests
{%- if cookiecutter.package_manager == "uv" %}
uv run pytest
{%- elif cookiecutter.package_manager == "poetry" %}
poetry run pytest
{%- else %}
pytest
{%- endif %}

# Run specific test
{%- if cookiecutter.package_manager == "uv" %}
uv run pytest tests/unit/test_agents.py::test_agent_creation
{%- elif cookiecutter.package_manager == "poetry" %}
poetry run pytest tests/unit/test_agents.py::test_agent_creation
{%- else %}
pytest tests/unit/test_agents.py::test_agent_creation
{%- endif %}

# Run tests with markers
{%- if cookiecutter.package_manager == "uv" %}
uv run pytest -m "not slow"
{%- elif cookiecutter.package_manager == "poetry" %}
poetry run pytest -m "not slow"
{%- else %}
pytest -m "not slow"
{%- endif %}
```

---

## Documentation

### Types of Documentation

1. **Code comments**: Explain complex logic
2. **Docstrings**: Document all public APIs
3. **README**: Keep project README updated
4. **User guides**: Document usage patterns
5. **Developer guides**: Document architecture and design

### Documentation Style

- Use clear, concise language
- Include code examples
- Keep examples up-to-date
- Use proper markdown formatting

### Building Documentation

If using Sphinx:

```bash
cd docs/
make html
```

---

## Submitting Changes

### Creating a Pull Request

1. **Push your branch** to your fork
2. **Go to GitHub** and create a pull request
3. **Fill out the PR template** completely
4. **Link related issues** using keywords (e.g., "Closes #123")

### PR Title Format

```text
<type>: <short description>
```

Example: `feat: add web scraping tool for agents`

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Other (please describe)

## Motivation and Context
Why is this change needed? What problem does it solve?

## How Has This Been Tested?
Describe the tests you ran

## Screenshots (if applicable)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No new warnings generated
```

### PR Best Practices

- **Keep PRs small** and focused
- **Write clear descriptions**
- **Respond to feedback** promptly
- **Update your PR** if upstream changes
- **Be patient** - reviews take time

---

## Review Process

### What to Expect

1. **Automated checks** run first (tests, linting)
2. **Code review** by maintainers
3. **Feedback and discussion**
4. **Revisions** if needed
5. **Approval and merge**

### Review Timeline

- **Initial response**: Within 3-5 days
- **Full review**: Within 1-2 weeks
- **Urgent fixes**: Prioritized

### Addressing Feedback

- Be receptive to suggestions
- Ask questions if feedback is unclear
- Make requested changes promptly
- Push updates to the same branch
- Mark conversations as resolved when addressed

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Email**: {{ cookiecutter.author_email }}

### Getting Help

- Check existing documentation first
- Search closed issues for similar problems
- Ask in GitHub Discussions
- Be specific when asking questions

### Recognition

Contributors are recognized in:

- `CONTRIBUTORS.md` file
- Release notes
- Project documentation

---

## License

By contributing, you agree that your contributions will be licensed under the {{ cookiecutter.license }} License.

---

## Questions?

If you have questions about contributing, please:

1. Check this guide and other documentation
2. Search existing issues and discussions
3. Create a new discussion or issue
4. Email: {{ cookiecutter.author_email }}

---

**Thank you for contributing to {{ cookiecutter.project_name }}!** 🎉

Your contributions help make this project better for everyone.
