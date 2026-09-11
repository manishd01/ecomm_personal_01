from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=os.environ["GEMINI_API_KEY"],
)


def rewrite_query(question: str) -> str:
    prompt = f"""
Rewrite the following customer question into a concise search query
for an e-commerce knowledge base.

Keep the original intent.
Use important keywords.
Do not answer the question.
Return only the rewritten query.

Customer question:
{question}
"""

    response = llm.invoke(prompt)

    if isinstance(response.content, list):
        return "".join(
            item.get("text", "") for item in response.content if isinstance(item, dict)
        ).strip()

    return response.content.strip()
