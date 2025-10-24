from fastapi import FastAPI, Request, Form
from fastapi.concurrency import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from .db import async_session, init_db
from .models import Person
from .schemas import PersonCreate

templates = Jinja2Templates(directory="app/templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup code
    print("Running startup tasks...")
    await init_db()
    yield
    # shutdown code (if any)

app = FastAPI(lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "success": False})


@app.post("/persons/new", response_class=HTMLResponse)
async def create_person(request: Request, first_name: str = Form(...), last_name: str = Form(...), email: str = Form(...)):
    # validate via pydantic
    person_in = PersonCreate(first_name=first_name, last_name=last_name, email=email)

    async with async_session() as session:
        db_person = Person(first_name=person_in.first_name, last_name=person_in.last_name, email=person_in.email)
        session.add(db_person)
        await session.commit()
        await session.refresh(db_person)

    return templates.TemplateResponse("form.html", {"request": request, "success": True, "person": db_person})

@app.get("/persons/{person_id}", response_class=HTMLResponse)
async def read_person(request: Request, person_id: int):
    async with async_session() as session:
        db_person = await session.get(Person, person_id)
        if db_person is None:
            return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
        return templates.TemplateResponse("person.html", {"request": request, "person": db_person})