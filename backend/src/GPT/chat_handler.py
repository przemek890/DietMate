import os
from typing import Generator, Optional
import groq
from immutables import Map
from pymongo import collection

from .prompts import DietPrompter

def ask_gpt(
    message: str, 
    original_language: str, 
    client: groq.Client, 
    collectionGPT: collection.Collection,
    session_id: str,
    file_name: Optional[str] = None, 
    file_content: Optional[str] = None,
    flags: Map = Map()
) -> Generator[str, None, None]:
    """
    Sends a message to GPT and yields responses.

    :param message: The user's message to process.
    :param original_language: The language of the original message.
    :param client: The Groq client instance for sending requests.
    :param file_name: Optional file name to include in the request context.
    :param file_content: Optional file content to include in the request context.
    :param flags: Optional flags to modify behavior or apply specific rules.
    :return: A generator yielding strings as responses.
    """

    flags = flags or Map()

    rule_types: dict[str, str] = {
        "gp": "general_principles",
        "sr": "security_rules",
        "cr": "coding_rules",
    }

    system_message: str = "***SYSTEM RULES***\n"
    for flag, rule_type in rule_types.items():
        if flags.get(flag, True):
            system_message += DietPrompter.get_rules(rule_type)

    system_message += "***PREVIOUS CONVERSATION HISTORY***:\n"
    system_message += DietPrompter.get_latest_records(collectionGPT, session_id)

    user_message: str = (
        "***USER MESSAGE***:\n"
        + DietPrompter.get_user_message(message, original_language)
        + DietPrompter.get_file_content(file_name, file_content)
    )
    
    model: str = os.getenv("GROQ_GPT_MODEL", "llama-3.3-70b-versatile")

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
            max_tokens=8000,
            top_p=0.5,
            stream=True,
            stop=None
        )
        for chunk in completion:
            yield chunk.choices[0].delta.content or ""

    except groq.RateLimitError:
        yield "***ERROR***: Rate limit exceeded. Please try again later."
    except Exception as e:
        yield f"***ERROR***: Unable to process request: {str(e)}"
