from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2", temperature=0)

SYSTEM_PROMPT = """You are an Enterprise AI Knowledge Assistant.

Instructions:
- Answer ONLY using the provided context.
- Give a direct, natural and professional answer.
- Do NOT start with phrases like "Based on the provided context" or "According to the context".
- If the answer is not available in the context, reply exactly:
  "I couldn't find that information in the uploaded documents."
- If the answer contains a list, format it as bullet points.
- Keep the response concise and easy to read."""


def _build_prompt(question: str, docs: list, history: list = None) -> str:
    context = "\n\n".join(doc.page_content for doc in docs)

    history_text = ""
    if history:
        history_text = "\n".join(
            f"{m.role.capitalize()}: {m.content}" for m in history[-6:]
        )
        history_text = f"\nConversation History:\n{history_text}\n"

    return f"""{SYSTEM_PROMPT}
{history_text}
Context:
{context}

Question:
{question}

Answer:"""


def rewrite_query(question: str, history: list) -> str:
    if not history:
        return question

    history_text = "\n".join(
        f"{m.role.capitalize()}: {m.content}" for m in history[-4:]
    )
    prompt = f"""Given this conversation history, rewrite the follow-up question as a standalone question.
Only return the rewritten question, nothing else.

History:
{history_text}

Follow-up question: {question}
Standalone question:"""

    response = llm.invoke(prompt)
    return response.content.strip()


def generate_answer(question: str, docs: list, history: list = None) -> str:
    response = llm.invoke(_build_prompt(question, docs, history))
    return response.content


def stream_answer(question: str, docs: list, history: list = None):
    for chunk in llm.stream(_build_prompt(question, docs, history)):
        yield chunk.content
