from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
from bs4 import BeautifulSoup
from requests_toolbelt.multipart.encoder import MultipartEncoder

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/tiktokdl")
def download_tiktok(url: str = Query(...)):
    base_url = "https://ttdownloader.co/"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    headers = {"User-Agent": user_agent}

    response = requests.get(base_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    token_input = soup.find("input", {"name": "_token"})
    token = token_input['value'] if token_input else ""

    cookies = response.cookies.get_dict()

    m = MultipartEncoder(
        fields={
            "_token": token,
            "url": url
        }
    )

    post_headers = {
        "User-Agent": user_agent,
        "Referer": base_url,
        "Content-Type": m.content_type
    }

    post_response = requests.post(f"{base_url}fetch", headers=post_headers, data=m, cookies=cookies)
    post_response.raise_for_status()
    data = post_response.json()

    downloads = data.get("downloadUrls", [])
    video_url = ""
    for video in downloads:
        if video.get("isHD"):
            video_url = video.get("url")
            break
    if not video_url and downloads:
        video_url = downloads[0].get("url")

    result = {
        "title": data.get("caption"),
        "username": data.get("author", {}).get("username"),
        "video_url": video_url,
        "mp3url": data.get("mp3URL")
    }

    return JSONResponse(content=result, indent=4)