"""Generation step of the RAG pipeline: build the grounded prompt, call the LLM."""

import asyncio
from pathlib import Path

from sage.domain.qa.models import Chunk
from sage.integrations.llm.generate import generate_text
from sage.integrations.storage.instructions import fetch_extra_instructions

_PROMPT_TEMPLATE = (Path(__file__).parent / "prompts" / "answer_prompt.txt").read_text(
    encoding="utf-8"
)
_NO_DOCUMENTS_CONTEXT = (
    "Nessun documento disponibile (base di conoscenza non ancora popolata o non configurata)."
)


def build_prompt(question: str, chunks: list[Chunk], extra_instructions: str = "") -> str:
    context = (
        "\n\n".join(f"[{chunk.source}] {chunk.text}" for chunk in chunks)
        if chunks
        else _NO_DOCUMENTS_CONTEXT
    )
    base_prompt = _PROMPT_TEMPLATE.format(context=context, question=question)
    if extra_instructions:
        return f"{extra_instructions}\n\n{base_prompt}"
    return base_prompt


async def generate_answer(question: str, chunks: list[Chunk]) -> str:
    extra_instructions = await asyncio.to_thread(fetch_extra_instructions)
    prompt = build_prompt(question, chunks, extra_instructions=extra_instructions)
    return await generate_text(prompt)
