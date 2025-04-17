from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from youtubesearchpython import VideosSearch
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

import random
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
#import uvicorn
from mangum import Mangum

app = FastAPI(
    title="YouTube Music Search API",
    description="FastAPI app to search music from YouTube with filtering, pagination, and caching.",
    version="2.0.0"
)

# Allow all origins (for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ThreadPool for blocking I/O
executor = ThreadPoolExecutor(max_workers=10)

# Categories for /home
categories = [
    "Bollywood Songs", "Lofi Beats", "Bhojpuri",
    "Punjabi Songs", "Haryanvi Songs", "Latest Songs"
]

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

logging.getLogger("uvicorn.access").setLevel(logging.ERROR)

# Utility to check if video is a song
def is_song(video):
    return video.get("duration") and video.get("channel", {}).get("name")

# Format video into a clean dict
def format_video(video):
    return {
        "title": video.get("title"),
        "url": video.get("link"),
        "thumbnail": video.get("thumbnails", [{}])[0].get("url"),
        "duration": video.get("duration"),
        "channel": video.get("channel", {}).get("name"),
    }

# Run blocking search
def search_youtube_sync(query: str, limit: int = 50):
    try:
        search = VideosSearch(query, limit=limit)
        return search.result().get("result", [])
    except Exception as e:
        logging.error(f"search_youtube_sync error: {e}")
        return []

# Async wrapper
async def search_youtube(query: str, limit: int = 50):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, search_youtube_sync, query, limit)

@app.on_event("startup")
async def setup_cache():
    FastAPICache.init(InMemoryBackend())

@app.get("/")
async def root():
    return {"message": "Welcome to the YouTube Music Search API!"}

# Serve favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/search")
async def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, gt=0, le=50),
    page: int = Query(1, gt=0),
    lang: str = Query(None)
):
    raw_query = f"{q} {lang} song" if lang else q
    all_results = await search_youtube(raw_query, 50)

    # Filter songs
    songs = [format_video(v) for v in all_results if is_song(v)]
    total = len(songs)

    # Paginate
    start = (page - 1) * limit
    end = start + limit
    paginated = songs[start:end]

    return {
        "results": paginated,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "has_more": end < total
        }
    }

@app.get("/home")
@cache(expire=300)
async def home():
    random.shuffle(categories)
    selected = categories[:5]

    tasks = [search_youtube(cat, 20) for cat in selected]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    home_feed = {}
    for cat, res in zip(selected, results):
        if isinstance(res, list):
            filtered = [format_video(v) for v in res if is_song(v)]
            home_feed[cat] = filtered[:5]

    return {"home_feed": home_feed}

# Export a handler for Vercel's Python runtime
handler = Mangum(app)

#if __name__ == "__main__":
#    uvicorn.run("main:app", reload=True)
