"""
Chat model factory. Switch provider or model with `LLM_MODEL` in `.env`.
"""

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from {{ cookiecutter.module_name }}.config import LLM_MODEL


def get_llm(model: str = LLM_MODEL) -> BaseChatModel:
    """
    Create a chat model.

    Parameters
    ----------
    model : str, optional
        Model as `"<provider>:<model>"` (default is `LLM_MODEL`).

    Returns
    -------
    langchain_core.language_models.BaseChatModel
        The chat model.
    """
    return init_chat_model(model)
