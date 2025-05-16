# Shoti API

Shoti API is a lightweight API built with **FastAPI** to retrieve random TikTok shawty videos with metadata, including the uploader's name, video title, and a direct download link (without a watermark).

---

## How It Works

1. **Random Video Selection**:
   - The API reads a list of TikTok video URLs from a JSON file (`shoti_videos.json`).
   - A random URL is selected from the list.

2. **Metadata Extraction**:
   - The API sends a request to `https://ssstik.io` to fetch metadata for the selected TikTok video.
   - Extracted metadata includes:
     - `author`: Uploader's name.
     - `title`: Video title or caption.
     - `video_url`: No-watermark direct download link.

3. **Response**:
   - The API returns the metadata in JSON format.

---

## Example JSON Response

Here’s an example of the JSON response you’ll get when hitting the `/shoti` endpoint:

```json
{
    "author": "JohnDoe",
    "title": "Check out this cool video!",
    "video_url": "https://example.com/video.mp4"
}
```

---

## Example: `shoti_videos.json`

This file contains a list of TikTok video URLs for the API to choose from:

```json
[
    "https://www.tiktok.com/@user/video/123456",
    "https://www.tiktok.com/@user/video/789012",
    "https://www.tiktok.com/@user/video/345678"
]
```

---

## Deployment

### Platforms

You can deploy the API on the following platforms:

1. **[Vercel](https://vercel.com/)**: `Recommended`
   - Vercel is a simple and scalable platform to deploy FastAPI apps.
   - Follow their [Python deployment guide](https://vercel.com/docs/concepts/functions/serverless-functions/python).

2. **[Render](https://render.com/)**:
   - Render supports deploying FastAPI apps directly from your repository.
   - Guide: [Render FastAPI Docs](https://render.com/docs/deploy-fastapi).

3. **[Railway](https://railway.app/)**:
   - Railway provides an easy way to deploy FastAPI apps.
   - Guide: [Deploy on Railway](https://docs.railway.app/deploy/fastapi).

### Steps to Deploy

1. **Push your repository to GitHub**:
   - Make sure your `main.py`, `shoti_videos.json`, and `requirements.txt` are committed and pushed.

2. **Choose a Deployment Platform**:
   - Select one of the platforms above and follow their deployment steps.

3. **Set Environment Variables (if needed)**:
   - Some platforms may require setting environment variables for specific configurations.

4. **Test the Deployment**:
   - Once deployed, visit the `/shoti` endpoint to test the API.

---

## Running Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/shoti-api.git
   cd shoti-api
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   uvicorn main:app --reload
   ```
   - The API will be available at `http://127.0.0.1:8000`.

---

## Author

**Kaizenega**.

Feel free to reach out through the [Contact Page](https://kaizenji-info.pages.dev) for feedback or contributions! 🐸