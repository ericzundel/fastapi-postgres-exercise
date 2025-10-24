from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from .db import async_session, init_db
from .models import Person
from .schemas import PersonCreate

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
async def startup_event():
    # create tables if needed
    await init_db()


@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "success": False})


@app.post("/person/new", response_class=HTMLResponse)
async def create_person(request: Request, first_name: str = Form(...), last_name: str = Form(...), email: str = Form(...)):
    # validate via pydantic
    person_in = PersonCreate(first_name=first_name, last_name=last_name, email=email)

    async with async_session() as session:
        db_person = Person(first_name=person_in.first_name, last_name=person_in.last_name, email=person_in.email)
        session.add(db_person)
        await session.commit()
        await session.refresh(db_person)

    return templates.TemplateResponse("form.html", {"request": request, "success": True, "person": db_person})
