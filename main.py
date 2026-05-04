from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Home
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    habits = db.query(models.Habit).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "habits": habits
    })


# Add habit
@app.post("/add")
def add_habit(name: str = Form(...), db: Session = Depends(get_db)):
    new_habit = models.Habit(name=name)
    db.add(new_habit)
    db.commit()
    return {"message": "Habit added"}


# Update streak
@app.post("/update/{habit_id}")
def update_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()

    if habit:
        habit.streak += 1
        db.commit()
        return {"message": "Updated"}

    return {"error": "Habit not found"}


# Add page
@app.get("/add-page")
def add_page(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})


# Progress page
@app.get("/progress")
def progress(request: Request, db: Session = Depends(get_db)):
    habits = db.query(models.Habit).all()
    return templates.TemplateResponse("progress.html", {
        "request": request,
        "habits": habits
    })