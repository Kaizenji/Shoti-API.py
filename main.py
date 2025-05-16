from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
import httpx
from bs4 import BeautifulSoup
import random
import json
import traceback
import os

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

        print("=== HTTPX DEBUG ===")
        print("Status Code:", response.status_code)
        print("Response Snippet:\n", response.text[:1000])  # Show first 1000 chars for debugging

        soup = BeautifulSoup(response.text, "html.parser")

        author_img = soup.select_one("img.result_author")
        author = author_img["alt"] if author_img else "Unknown"

        title_tag = soup.select_one("#avatarAndTextUsual p.maintext")
        title = title_tag.text.strip() if title_tag else "Untitled"

        download_link = soup.select_one("a.download_link.without_watermark")
        video_url = download_link["href"] if download_link else None

        if not video_url:
            raise Exception("Video URL not found in HTML response.")

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
        if not os.path.exists("shoti_videos.json"):
            raise FileNotFoundError("shoti_videos.json file is missing.")

        with open("shoti_videos.json", "r") as file:
            urls = json.load(file)

        if not isinstance(urls, list) or not urls:
            raise HTTPException(status_code=404, detail="No valid URLs found in JSON file.")

        random_url = random.choice(urls)
        print(f"Selected TikTok URL: {random_url}")

        data = await fetch_tiktok_data(random_url)

        # Return pretty-printed JSON
        return Response(
            content=json.dumps(data, indent=4),
            media_type="application/json"
        )

    except FileNotFoundError as fnf_error:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(fnf_error))

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to fetch video data: {str(e)}")