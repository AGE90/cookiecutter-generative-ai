# Installation Guide

This guide covers installation for {{ cookiecutter.project_name }} using different package managers.

---

## Prerequisites

Before installing, ensure you have:

- **Python {{ cookiecutter.python_version }}** or higher
- **Git** (for cloning the repository)
{%- if cookiecutter.package_manager == "uv" %}
- **uv** package manager
{%- elif cookiecutter.package_manager == "poetry" %}
- **Poetry** package manager
{%- elif cookiecutter.package_manager == "pip-tools" %}
- **pip-tools** package
{%- endif %}

### Python Installation

If you don't have Python installed:

**Windows:**

```bash
# Download from python.org or use winget
winget install Python.Python.{{ cookiecutter.python_version.split('.')[0] }}.{{ cookiecutter.python_version.split('.')[1] }}
```

**macOS:**

```bash
# Using Homebrew
brew install python@{{ cookiecutter.python_version }}
```

**Linux:**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python{{ cookiecutter.python_version }} python{{ cookiecutter.python_version }}-venv

# Fedora
sudo dnf install python{{ cookiecutter.python_version }}
```

---

{%- if cookiecutter.package_manager == "uv" %}

## Installation with uv (Recommended)

### 1. Install uv

**Windows:**

```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Alternative (via pip):**

```bash
pip install uv
```

### 2. Clone the Repository

```bash
git clone {{ cookiecutter.project_url }}
cd {{ cookiecutter.project_slug }}
```

### 3. Install Dependencies

```bash
# Install all dependencies
uv sync

# Or install specific groups
uv sync --group dev      # Development dependencies
uv sync --group test     # Testing dependencies
```

### 4. Verify Installation

```bash
uv run python --version
uv run python -c "import {{ cookiecutter.module_name }}; print('Installation successful!')"
```

### 5. Run Your Application

```bash
# Run Python scripts
uv run python script.py

# Run module
uv run python -m {{ cookiecutter.module_name }}

# Run with environment activation
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python script.py
```

### Common uv Commands

```bash
uv add package-name              # Add a package
uv add --dev package-name        # Add dev package
uv remove package-name           # Remove a package
uv sync                          # Sync environment
uv lock                          # Update lock file
uv run python script.py          # Run with uv
```

{%- elif cookiecutter.package_manager == "poetry" %}

## Installation with Poetry

### 1. Install Poetry

**Windows (PowerShell):**

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

**macOS/Linux:**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Alternative (via pip):**

```bash
pip install poetry
```

### 2. Configure Poetry (Optional)

```bash
# Create virtual environments in project directory
poetry config virtualenvs.in-project true
```

### 3. Clone the Repository

```bash
git clone {{ cookiecutter.project_url }}
cd {{ cookiecutter.project_slug }}
```

### 4. Install Dependencies

```bash
# Install all dependencies
poetry install

# Install without dev dependencies
poetry install --without dev

# Install specific groups
poetry install --with test
```

### 5. Activate the Environment

```bash
# Activate virtual environment
poetry shell

# Or run commands directly
poetry run python script.py
```

### 6. Verify Installation

```bash
poetry run python --version
poetry run python -c "import {{ cookiecutter.module_name }}; print('Installation successful!')"
```

### Common Poetry Commands

```bash
poetry add package-name                    # Add a package
poetry add --group dev package-name        # Add dev package
poetry remove package-name                 # Remove a package
poetry update                              # Update dependencies
poetry show                                # List packages
poetry shell                               # Activate environment
poetry run python script.py                # Run with poetry
```

{%- elif cookiecutter.package_manager == "pip-tools" %}

## Installation with pip-tools

### 1. Install pip-tools

```bash
pip install pip-tools
```

### 2. Clone the Repository

```bash
git clone {{ cookiecutter.project_url }}
cd {{ cookiecutter.project_slug }}
```

### 3. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
# Sync to exact versions in requirements-dev.txt
pip-sync requirements-dev.txt

# Or install production dependencies only
pip-sync requirements.txt
```

### 5. Verify Installation

```bash
python --version
python -c "import {{ cookiecutter.module_name }}; print('Installation successful!')"
```

### 6. Run Your Application

```bash
# Ensure virtual environment is activated
python script.py
python -m {{ cookiecutter.module_name }}
```

### Common pip-tools Commands

```bash
# Edit requirements.in or requirements-dev.in, then:
pip-compile requirements.in                      # Compile requirements
pip-compile requirements-dev.in                  # Compile dev requirements
pip-compile --upgrade requirements.in            # Upgrade dependencies
pip-sync requirements-dev.txt                    # Sync environment
```

### Managing Dependencies

1. **Add a new package:**
   - Edit `requirements.in` (production) or `requirements-dev.in` (dev)
   - Add the package name: `new-package>=1.0.0`
   - Compile: `pip-compile requirements.in`
   - Sync: `pip-sync requirements-dev.txt`

2. **Update packages:**

   ```bash
   pip-compile --upgrade requirements.in
   pip-sync requirements-dev.txt
   ```

{%- elif cookiecutter.package_manager == "pip" %}

## Installation with pip

### 1. Clone the Repository

```bash
git clone {{ cookiecutter.project_url }}
cd {{ cookiecutter.project_slug }}
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Or install with development dependencies
pip install -r requirements-dev.txt
```

### 4. Verify Installation

```bash
python --version
python -c "import {{ cookiecutter.module_name }}; print('Installation successful!')"
```

### 5. Run Your Application

```bash
# Ensure virtual environment is activated
python script.py
python -m {{ cookiecutter.module_name }}
```

### Common pip Commands

```bash
pip install package-name              # Install a package
pip install -r requirements.txt       # Install from requirements
pip freeze > requirements.txt         # Save current packages
pip list                              # List installed packages
pip show package-name                 # Show package info
pip uninstall package-name            # Uninstall a package
```

### Managing Dependencies

1. **Add a new package:**

   ```bash
   pip install new-package
   pip freeze > requirements.txt  # Update requirements file
   ```

2. **Update packages:**

   ```bash
   pip install --upgrade package-name
   pip freeze > requirements.txt
   ```

{%- else %}

## Installation (Manual Setup)

### 1. Clone the Repository

```bash
git clone {{ cookiecutter.project_url }}
cd {{ cookiecutter.project_slug }}
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies Manually

Install the required packages:

```bash
pip install langchain langgraph python-dotenv requests pydantic
```

For development:

```bash
pip install pytest pytest-cov pytest-mock ruff black isort mypy
```

### 4. Verify Installation

```bash
python --version
python -c "import {{ cookiecutter.module_name }}; print('Installation successful!')"
```

{%- endif %}

---

## Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example
cp .env.example .env

# Edit with your values
nano .env  # or use your preferred editor
```

Example `.env` file:

```bash
# API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Model Configuration
DEFAULT_MODEL=gpt-4
TEMPERATURE=0.7
MAX_TOKENS=2000

# Application Settings
DEBUG=false
LOG_LEVEL=INFO
```

---

## IDE Setup

### VS Code

1. Install Python extension
2. Select interpreter:
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Python: Select Interpreter"
   - Choose the virtual environment (`.venv`)

3. Recommended extensions:
   - Python
   - Pylance
   - Ruff
   - Jupyter (for notebooks)

### PyCharm

1. Open project in PyCharm
2. Configure interpreter:
   - Go to Settings → Project → Python Interpreter
   - Click gear icon → Add
   - Select "Existing environment"
   - Choose `.venv/bin/python` (or `.venv\Scripts\python.exe` on Windows)

---

## Jupyter Notebooks

To use Jupyter notebooks:

{%- if cookiecutter.package_manager == "uv" %}

```bash
uv add --dev jupyter ipykernel
uv run jupyter notebook
```

{%- elif cookiecutter.package_manager == "poetry" %}

```bash
poetry add --group dev jupyter ipykernel
poetry run jupyter notebook
```

{%- else %}

```bash
pip install jupyter ipykernel
jupyter notebook
```

{%- endif %}

Or use VS Code's built-in notebook support.

---

## Troubleshooting

### Common Issues

**Issue: Command not found**

```bash
# Ensure package manager is in PATH
# For uv:
echo $PATH | grep uv  # Should show uv path

# For poetry:
poetry --version  # Should show version
```

**Issue: Python version mismatch**

```bash
# Check Python version
python --version

# Specify Python version explicitly (with uv):
uv python install {{ cookiecutter.python_version }}
uv python pin {{ cookiecutter.python_version }}
```

**Issue: Import errors**

```bash
# Verify installation
{%- if cookiecutter.package_manager == "uv" %}
uv run pip list
{%- elif cookiecutter.package_manager == "poetry" %}
poetry show
{%- else %}
pip list
{%- endif %}

# Reinstall if needed
{%- if cookiecutter.package_manager == "uv" %}
uv sync --reinstall
{%- elif cookiecutter.package_manager == "poetry" %}
poetry install --sync
{%- else %}
pip install -r requirements.txt --force-reinstall
{%- endif %}
```

**Issue: Permission errors**

```bash
# Don't use sudo with package managers
# Instead, ensure proper ownership:
sudo chown -R $USER:$USER ~/.local  # For uv/pip
```

### Getting Help

- Check the [FAQ](docs/faq.md)
- Open an issue: {{ cookiecutter.project_url }}/issues
- Email: {{ cookiecutter.author_email }}

---

## Next Steps

After installation:

1. Read the [User Guide](user_guide.md)
2. Explore [Examples](../examples/)
3. Check [API Reference](api_reference.md)
4. Review [Developer Guide](developer_guide.md) if contributing

---

## Uninstallation

{%- if cookiecutter.package_manager == "uv" %}

```bash
# Remove virtual environment
rm -rf .venv

# Uninstall uv (optional)
uv self uninstall
```

{%- elif cookiecutter.package_manager == "poetry" %}

```bash
# Remove virtual environment
poetry env remove python

# Or manually
rm -rf .venv

# Uninstall poetry (optional)
curl -sSL https://install.python-poetry.org | python3 - --uninstall
```

{%- else %}

```bash
# Simply remove the virtual environment
rm -rf .venv  # Linux/macOS
# or
rmdir /s .venv  # Windows
```

{%- endif %}
