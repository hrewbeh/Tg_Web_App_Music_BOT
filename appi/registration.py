import os
import sys

from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(0, dir)

from database import engine, new_session
from models import Model, User

registration = APIRouter()
templates = Jinja2Templates(directory='templates')

Model.metadata.create_all(bind=engine)


def get_db():
    db = new_session()
    try:
        yield db
    finally:
        db.close()


@registration.get('/', response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('index.html', {
        'request': request
    })

@registration.get('/registration', response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('base.html', {
        'request': request
    })


@registration.post('/registration', response_class=HTMLResponse)
def registration_users(tg_id: int = Form(...), name: str = Form(...), password: str = Form(...), email: str = Form(...),
                       db: Session = Depends(get_db)):
    existing_user_by_email = db.query(User).filter(User.email == email).first()
    if existing_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_user_by_tg_id = db.query(User).filter(User.tg_id == tg_id).first()
    if existing_user_by_tg_id:
        raise HTTPException(status_code=400, detail="tg already registered")

    db_user = User(tg_id=tg_id, username=name, password=password, email=email)
    db.add(db_user)
    db.commit()
    return RedirectResponse(url=f'personal_area/{tg_id}', status_code=303)


@registration.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@registration.post("/login", response_class=HTMLResponse)
def login_user(request: Request, name: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == name).first()
    if existing_user and existing_user.password == password:
        return RedirectResponse(url=f'/personal_area/{existing_user.tg_id}', status_code=303)
    else:
        return templates.TemplateResponse('login.html', {'request': request})


@registration.get("/personal_area/{tg_id}", response_class=HTMLResponse)
def area(request: Request, tg_id: int, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.tg_id == tg_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="Not Found")
    return templates.TemplateResponse('personal_area.html', {'request': request, 'user': existing_user})


@registration.get("/static/media/{username}/")
def list_user_media(username: str):
    user_dir = f"media/{username}/"
    if not os.path.exists(user_dir):
        raise HTTPException(status_code=404, detail="User media directory not found")
    files = os.listdir(user_dir)
    return files


@registration.get("/recovery", response_class=HTMLResponse)
def recovery(request: Request, email: str = Form(...), db: Session = Depends(get_db)):
    # Тут логика отправки сообщения через емайл и отпавка нового пароля
    pass


@registration.delete("/delete")
def delete(request: Request, db: Session = Depends(get_db), tg_id: str = Form(...)):
    existing_user = db.query(User).filter(User.tg_id == tg_id).first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(existing_user)
    db.commit()
    return {"message": "User deleted successfully"}
