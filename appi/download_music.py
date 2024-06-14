import os

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pytube import Search, YouTube
from jinja2 import Template

from database import engine, new_session
from models import Model

download = APIRouter()
templates = Jinja2Templates(directory='templates')

Model.metadata.create_all(bind=engine)


def get_db():
    db = new_session()
    try:
        yield db
    finally:
        db.close()

user_data = {
    "username": "123123",
    "tg_id": "123",
    "email": "123"
}


@download.post('/download', response_class=HTMLResponse)
async def download_music(request: Request, query: str = Form(...), tg_id: str = Form(...)):
    result_search = Search(query)
    if len(result_search.results) > 0:
        url = f'https://www.youtube.com/watch?v={result_search.results[0].video_id}'
        yt = YouTube(url)
        output_path = f'media/{tg_id}'
        try:
            os.mkdir(output_path)
        except FileExistsError:
            pass
        
        video = yt.streams.filter(only_audio=True).first()
        downloaded_file = video.download(output_path=output_path)
        base, ext = os.path.splitext(downloaded_file)
        new_file = base + '.mp3'
        os.rename(downloaded_file, new_file)
        
        tracks = [f'media/{tg_id}/{f}' for f in os.listdir(output_path) if f.endswith('.mp3')]
        
        template = Template(open('personal_area.html').read())
        return template.render(user=user_data, tracks=tracks)


def delete(query: str, tg_id: str):
    path = f'C:/Users/Я/PycharmProjects/tg_vk_api_for_pars/media/{tg_id}'
    os.path.normpath(path)
    os.remove(path + "/" + query + '.mp3')
    if os.path.getsize(path):
        return None
    os.remove(path)


@download.delete('/delete_music', response_class=HTMLResponse)
async def delete_music(query, tg_id):
    delete(query, tg_id)
