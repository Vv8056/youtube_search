# from fastapi import FastAPI, Query
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from youtubesearchpython import VideosSearch
# import random
# import asyncio
# from concurrent.futures import ThreadPoolExecutor
# import uvicorn
# import logging

# app = FastAPI(
#     title="YouTube Music Search API",
#     description="A simple FastAPI app to fetch music data from YouTube using YouTubeSearchPython.",
#     version="1.0.0"
# )

# # Allow all origins for development (change in production)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Or replace with specific origins like ["http://localhost:3000"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Optional: Reduce logging noise for production
# logging.getLogger("uvicorn.access").setLevel(logging.ERROR)

# # Predefined categories for home feed
# categories = [
#     "Bollywood Songs", "Lofi Beats", "bhojpuri",
#     "Punjabi Songs", "Romantic Songs", "Latest Songs"
# ]

# # ThreadPoolExecutor for running blocking YouTube search calls
# executor = ThreadPoolExecutor(max_workers=10)

# # Blocking YouTube search function
# def search_youtube_sync(query: str, limit: int = 50):
#     try:
#         videos_search = VideosSearch(query, limit=limit)
#         results = videos_search.result().get('result', [])
#         return [{
#             'title': video.get('title'),
#             'url': video.get('link'),
#             'thumbnail': video.get('thumbnails', [{}])[0].get('url'),
#             'duration': video.get('duration'),
#             'channel': video.get('channel', {}).get('name')
#         } for video in results]
#     except Exception as e:
#         logging.error(f"Error in search_youtube_sync: {e}")
#         return []

# # Async wrapper for running sync function in thread executor
# async def search_youtube(query: str, limit: int = 50):
#     loop = asyncio.get_event_loop()
#     return await loop.run_in_executor(executor, search_youtube_sync, query, limit)

# @app.get("/")
# async def index():
#     return {"message": "Welcome to the YouTube Music Search API (FastAPI Version)!"}

# @app.get("/search")
# async def search(q: str = Query(..., min_length=1)):
#     results = await search_youtube(q)
#     return {"results": results}

# @app.get("/home")
# async def home():
#     random.shuffle(categories)
#     selected = categories[:5]

#     # Run YouTube searches concurrently
#     tasks = [search_youtube(category, 20) for category in selected]
#     results = await asyncio.gather(*tasks, return_exceptions=True)

#     home_data = {
#         category: result if isinstance(result, list) else []
#         for category, result in zip(selected, results)
#     }

#     return {"home_feed": home_data}

# # Optional: Allow running with python main.py
# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)


from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from youtubesearchpython import VideosSearch
import random
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
from mangum import Mangum  # For Vercel compatibility

app = FastAPI(
    title="YouTube Music Search API",
    description="FastAPI app to search YouTube music content with support for pagination, language filtering, and streaming.",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.getLogger("uvicorn.access").setLevel(logging.ERROR)

# Predefined home page categories
categories = [
    "Bollywood Songs", "Lofi Beats", "bhojpuri",
    "Punjabi Songs", "Romantic Songs", "Latest Songs"
]

executor = ThreadPoolExecutor(max_workers=10)

# Blocking search function
def search_youtube_sync(query: str, limit: int = 20):
    try:
        search = VideosSearch(query, limit=limit)
        result = search.result().get("result", [])
        return [
            {
                "title": v.get("title"),
                "url": v.get("link"),
                "thumbnail": v.get("thumbnails", [{}])[0].get("url"),
                "duration": v.get("duration"),
                "channel": v.get("channel", {}).get("name")
            }
            for v in result
        ]
    except Exception as e:
        logging.error(f"[search_youtube_sync] {e}")
        return []

# Async wrapper
async def search_youtube(query: str, limit: int = 20):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, search_youtube_sync, query, limit)

@app.get("/")
async def index():
    return {"message": "Welcome to the YouTube Music Search API!"}

@app.get("/search")
async def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
    page: int = Query(1, ge=1),
    lang: str = Query(None)
):
    query = q + (f" {lang}" if lang else "")
    start = (page - 1) * limit
    results = await search_youtube(query, limit=limit + start)
    paginated = results[start:start + limit]

    return {
        "results": paginated,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": len(results),
            "has_more": len(results) > start + limit
        }
    }

@app.get("/home")
async def home():
    random.shuffle(categories)
    selected = categories[:5]
    tasks = [search_youtube(cat, 10) for cat in selected]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return {
        "home_feed": {
            cat: res if isinstance(res, list) else []
            for cat, res in zip(selected, results)
        }
    }

# Vercel deployment handler
handler = Mangum(app)
