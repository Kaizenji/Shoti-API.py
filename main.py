from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import httpx
from bs4 import BeautifulSoup
import random
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

async def fetch_tiktok_data(url: str):
    data = {
        "id": url,
        "locale": "en",
        "tt": ""
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
        "origin": "https://ssstik.io",
        "referer": "https://ssstik.io/",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://ssstik.io/abc?url=dl",
            data=data,
            headers=headers
        )
        soup = BeautifulSoup(response.text, "html.parser")

        author_img = soup.select_one("img.result_author")
        author = author_img["alt"] if author_img else None

        title_tag = soup.select_one("#avatarAndTextUsual p.maintext")
        title = title_tag.text.strip() if title_tag else None

        download_link = soup.select_one("a.download_link.without_watermark")
        video_url = download_link["href"] if download_link else None

        return {
            "author": author,
            "title": title,
            "video_url": video_url
        }

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/shoti")
async def shoti_random():
    try:
        with open("shoti_videos.json", "r") as file:
            urls = json.load(file)

        if not urls:
            raise HTTPException(status_code=404, detail="No URLs found in JSON file")

        random_url = random.choice(urls)
        data = await fetch_tiktok_data(random_url)
        return JSONResponse(content=data, indent=4)

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="shoti_videos.json file not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch video data")