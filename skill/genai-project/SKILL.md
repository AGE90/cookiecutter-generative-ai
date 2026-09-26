---
name: genai-project
description: Scaffold a new generative AI / LLM agent Python project (LangGraph tool-calling agent, FastAPI /chat endpoint, CLI, offline tests with a fake LLM, uv, ruff, mypy) from the AGE90 cookiecutter template with a single command. Use when the user asks to create, start, bootstrap, or scaffold a new generative AI, LLM, agent, chatbot, LangChain or LangGraph project.
---

# Scaffold a generative AI project

The template writes every file. Do NOT write project files yourself, and do NOT read the generated files back after it finishes. That's the point of this skill: one command instead of dozens of file writes.

## Steps

1. **Collect the answers.** Infer them from the request. Ask one short question only for what you can't infer; `project_name` is the only one that really matters. Everything else has a sensible default (table below).
   - Take the author details from `git config user.name` and `git config user.email` unless the user gave them.
   - Map the provider the user mentions to `llm_provider`: Claude/Anthropic -> `anthropic`, GPT/OpenAI -> `openai`, local/Llama/Ollama -> `ollama`.
   - Extra libraries the user mentions go in `extra_dependencies` (comma-separated). It's added on top of the defaults, so never repeat a default list just to add one package.
2. **Run one command** from the directory where the project should be created (or pass `-o <dir>`):

   ```bash
   uvx cookiecutter gh:AGE90/cookiecutter-generative-ai --no-input \
     project_name="Support Agent" \
     project_description="Answer customer questions" \
     author_name="..." author_email="..." \
     llm_provider=anthropic \
     extra_dependencies="langchain-community"
   ```

   - Pass only keys that differ from the defaults. Quote every value.
   - If the current directory is the template repo itself, use `.` instead of `gh:AGE90/cookiecutter-generative-ai`.
   - The post-gen hook runs `uv add` for each group, so it needs network access and takes a minute or two. Don't cancel it.
3. **Report back** in 2 or 3 lines: the created path (`./<project_slug>`), the provider, and the next steps: add the API key to `<project_slug>/.env`, then `make run Q="..."` or `make serve`.

Never write, ask for, or echo an API key yourself; the user adds it to `.env`.

## Options (`cookiecutter.json`)

| Key | Default | Notes |
|---|---|---|
| `project_name` | `My Project` | Human name. Slug and module are derived from it |
| `project_slug` | derived: lowercase, spaces/`_` to `-` | Directory name and CLI command. Lowercase letters, digits, single hyphens |
| `module_name` | derived: lowercase, spaces/`-` to `_` | Must be a valid Python identifier |
| `project_description` | `A one-line summary of the project` | |
| `author_name` | `Your name` | |
| `author_email` | `you@example.com` | Must be a valid email or generation fails |
| `project_version` | `0.1.0` | |
| `project_url` | `https://example.com` | Must be a valid URL (scheme + host) |
| `python_version` | `3.12` | Format `3.X`, minimum `3.11` |
| `license` | `MIT` | `MIT`, `Apache-2.0`, `BSD-3-Clause`, `GPL-3.0-or-later`, `No license file` |
| `llm_provider` | `anthropic` | `anthropic` (claude-opus-5), `openai` (gpt-5), `ollama` (llama3.2, local, no key). Sets the LangChain package, default `LLM_MODEL` and `.env` key |
| `initialize_env` | `yes` | `uv add` all dependency groups. `no` = files only, nothing installed |
| `project_dependencies` | `langchain, langgraph, fastapi, uvicorn[standard], python-dotenv, pyprojroot` | Main deps; the template code needs all of them. Don't override, use `extra_dependencies` |
| `extra_dependencies` | empty | Added to the main deps on top of the defaults. **Use this for any extra library the user asks for** |
| `development_dependencies` | `mypy, ruff, pre-commit, ipykernel` | `dev` group |
| `testing_dependencies` | `pytest, pytest-cov, httpx` | `test` group (`httpx` is needed by FastAPI's test client) |
| `initialize_git_repository` | `yes` | `git init` plus an initial commit |

## If it fails

- `ERROR: ...` comes from the pre-gen validation: fix that value and rerun. Nothing was created.
- Hook failure (uv, git): the files were already generated. Report the error. Don't delete the directory without asking.
- `uvx` not found: install uv (`curl -LsSf https://astral.sh/uv/install.sh | sh`) or use `pipx run cookiecutter ...`.
