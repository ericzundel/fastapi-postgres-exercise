import logging
import time

from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from .db import async_session, init_db
from .models import Person
from .schemas import PersonCreate
from .asgi_middleware import ASGILogBodyMiddleware

#############################################
# Application setup


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="app/templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup code
    print("Running startup tasks...")
    await init_db()
    yield
    # shutdown code (if any)

app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    response_time = time.perf_counter() - start_time
    logger.info(f"{request.method} {request.url.path} {response.status_code} {response_time:.3f}s")
    logger.debug(f". Headers: {request.headers}")
    return response


######################################################
# Routes
@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "success": False})


@app.post("/persons/new")
async def create_person(person_in: PersonCreate, request: Request):
    """Accept JSON body (PersonCreate), persist to DB, and return the created person as JSON.

    The UI (form.html) will POST JSON with Content-Type: application/json.
    """
    async with async_session() as session:
        db_person = Person(first_name=person_in.first_name, last_name=person_in.last_name, email=person_in.email)
        session.add(db_person)
        await session.commit()
        await session.refresh(db_person)

    # Return a plain dict; FastAPI will JSON-serialize it.
    return {
        "id": db_person.id,
        "first_name": db_person.first_name,
        "last_name": db_person.last_name,
        "email": db_person.email,
    }

@app.get("/persons/{person_id}", response_class=HTMLResponse)
async def read_person(request: Request, person_id: int):
    async with async_session() as session:
        db_person = await session.get(Person, person_id)
        if db_person is None:
            return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
        return templates.TemplateResponse("person.html", {"request": request, "person": db_person})
    
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Wrap the FastAPI app with ASGI middleware that logs request bodies and
# replays the receive stream so route handlers can still consume the body.
# NB(zundel): Might be useful, but throws exceptions all over the place
# app = ASGILogBodyMiddleware(app)