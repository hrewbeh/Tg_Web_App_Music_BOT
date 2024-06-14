import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from download_music import download
from registration import registration

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(registration)
app.include_router(download)


def run_server_fastapi():
    uvicorn.run(app)


if __name__ == '__main__':
    run_server_fastapi()
