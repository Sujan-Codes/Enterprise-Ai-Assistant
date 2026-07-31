from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2", temperature=0)

SYSTEM_PROMPT = """You are an Enterprise AI Knowledge Assistant.

Rules:
- Answer ONLY from the supplied document context below.
- NEVER use your own training knowledge.
- NEVER explain topics generally (e.g. what education means, what a resume is).
- If the user asks about resume, education, skills, experience, projects, certifications, or summary — extract that information ONLY from the context.
- If the information is not present in the context, reply exactly: "I couldn't find that information in the uploaded document."
- Format lists as bullet points.
- Keep answers concise and professional.
- Do NOT start with phrases like "Based on the context" or "According to the document"."""


def _build_prompt(question: str, docs: list, history: list = None) -> str:
    if not docs:
        return f"{SYSTEM_PROMPT}\n\nContext:\n[No relevant content found in the uploaded document.]\n\nQuestion:\n{question}\n\nAnswer:"

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
    history_text = ""
    if history:
        history_text = "\n".join(
            f"{m.role.capitalize()}: {m.content}" for m in history[-4:]
        )
        history_text = f"Conversation History:\n{history_text}\n\n"

    prompt = f"""You are rewriting a user question into a precise document search query.

Rules:
- Resolve pronouns using the conversation history.
- Convert vague questions into specific document-retrieval queries.
- Never answer the question — only return the rewritten search query.

Examples:
  "tell me what is in resume" → "Summarize the uploaded resume"
  "tell the education" → "Education section of the resume"
  "what are the skills" → "Skills section of the resume"
  "tell the experience" → "Work Experience section of the resume"
  "what projects are mentioned" → "Projects section of the resume"
  "what are its benefits" (after Salesforce) → "Benefits of Salesforce"

{history_text}Question: {question}
Search query:"""

    response = llm.invoke(prompt)
    return response.content.strip()


def generate_answer(question: str, docs: list, history: list = None) -> str:
    response = llm.invoke(_build_prompt(question, docs, history))
    return response.content


def stream_answer(question: str, docs: list, history: list = None):
    for chunk in llm.stream(_build_prompt(question, docs, history)):
        yield chunk.content
