"""
Settings, read from environment variables or the `.env` file (see `.env.example`).
"""

import os

from dotenv import load_dotenv

from {{ cookiecutter.module_name }}.utils.paths import project_dir

load_dotenv(project_dir(".env"))

# "<provider>:<model>", passed to LangChain's `init_chat_model`
LLM_MODEL = os.getenv("LLM_MODEL", "{{ cookiecutter._default_models[cookiecutter.llm_provider] }}")
