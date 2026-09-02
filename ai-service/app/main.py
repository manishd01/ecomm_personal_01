import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware


from fastapi import FastAPI
from pydantic import BaseModel

from app.ingest import ingest_file, ingest_knowledge
from app.rag import answer_question

KNOWLEDGE_DIR = Path("/app/knowledge")


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]


async def watch_knowledge():

    last_state = {}

    while True:

        current_state = {}

        for file_path in KNOWLEDGE_DIR.glob("*.md"):

            current_state[str(file_path)] = file_path.stat().st_mtime_ns

        if not last_state:

            last_state = current_state

            print(
                "Initial knowledge state recorded.",
                flush=True,
            )

        else:

            changed_files = []

            for file_path in KNOWLEDGE_DIR.glob("*.md"):

                path = str(file_path)

                old_mtime = last_state.get(path)
                new_mtime = current_state.get(path)

                if old_mtime != new_mtime:

                    changed_files.append(file_path)

            for file_path in changed_files:

                print(
                    f"Knowledge changed: {file_path.name}",
                    flush=True,
                )

                try:

                    await asyncio.to_thread(
                        ingest_file,
                        file_path,
                    )

                    print(
                        f"Automatic ingestion completed: " f"{file_path.name}",
                        flush=True,
                    )

                except Exception as e:

                    print(
                        f"Automatic ingestion failed for " f"{file_path.name}: {e}",
                        flush=True,
                    )

            last_state = current_state

        await asyncio.sleep(2)


@asynccontextmanager
async def lifespan(app: FastAPI):

    await asyncio.to_thread(ingest_knowledge)

    watcher = asyncio.create_task(watch_knowledge())

    print(
        "Knowledge watcher started.",
        flush=True,
    )

    yield

    watcher.cancel()

    try:
        await watcher
    except asyncio.CancelledError:
        pass

    print(
        "Knowledge watcher stopped.",
        flush=True,
    )


app = FastAPI(
    title="E-commerce AI Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():

    return {
        "status": "healthy",
        "service": "ai-service",
    }


@app.post(
    "/api/ai/ask",
    response_model=ChatResponse,
)
def ask(request: ChatRequest):

    return answer_question(request.question)


# createt  id = 14  |     order_number = ORD-000014    | thiiswayyy


# docker compose --env-file .env.development -f docker-compose.yml -f docker-compose.dev.yml build --no-cache ai-service    ----building containnere.....
# docker compose --env-file .env.development -f docker-compose.yml -f docker-compose.dev.yml up ai-service                   ====s tarting ctonianer:
