# 🎵 YouTube Music Search API 🎶

A blazing-fast 🔥 FastAPI-powered backend that searches music videos from YouTube using [`youtube-search-python`](https://github.com/alexmercerind/youtube-search-python), with features like pagination, category feed, language filtering, and in-memory caching. Ideal for building lightweight music apps, search tools, or personalized home feeds!

---

## 🚀 Live Demo (Vercel)
> 🔗 Coming soon: [your-vercel-url.vercel.app](https://your-vercel-url.vercel.app)

---

## 🧠 Features

✅ Search YouTube for music videos  
✅ Filter by language and paginate results  
✅ Curated `/home` category feed  
✅ Blazing fast with `ThreadPoolExecutor`  
✅ Caching support with `fastapi-cache`  
✅ CORS enabled for easy frontend integration  
✅ Ready for Vercel deployment 🚀  

---

## 📦 Tech Stack

- ⚡ **FastAPI** – Python async web framework  
- 🔍 **youtube-search-python** – Search and scrape YouTube content  
- 📂 **fastapi-cache2** – Caching search results (in-memory)  
- 🧥 **ThreadPoolExecutor** – Background thread handling for I/O  
- 🌍 **CORS Middleware** – Cross-origin access for frontend use  
- 🌐 **Vercel** – Seamless serverless deployment

---

## 🛠️ Setup & Run Locally

```bash
# Clone the repo
git clone https://github.com/your-username/youtube-music-search-api
cd youtube-music-search-api

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload
```

---

## 📆 Requirements

```
fastapi==0.110.2
uvicorn==0.29.0
youtubesearchpython==1.6.6
fastapi-cache2==0.2.1
mangum==0.17.0
```

---

## 🔌 API Endpoints

### `GET /`
Health check & welcome message.
```json
{
  "message": "Welcome to the YouTube Music Search API!"
}
```

---

### `GET /search`
Search YouTube for songs.

#### Query Params:
| Name | Type | Description |
|------|------|-------------|
| `q` | string | 🔍 Search query (required) |
| `limit` | int | Number of results per page (1–50) |
| `page` | int | Page number (pagination) |
| `lang` | string | Optional language filter (e.g. Hindi) |

#### Example:
```
GET /search?q=arijit+singh&lang=Hindi&limit=10&page=2
```

#### Response:
```json
{
  "results": [
    {
      "title": "Tum Hi Ho - Aashiqui 2",
      "url": "https://youtube.com/watch?v=abcd1234",
      "thumbnail": "https://i.ytimg.com/vi/abcd1234/hqdefault.jpg",
      "duration": "4:22",
      "channel": "T-Series"
    }
  ],
  "pagination": {
    "page": 2,
    "limit": 10,
    "total": 48,
    "has_more": true
  }
}
```

---

### `GET /home`
Curated music categories like Bollywood, Lofi, Punjabi, etc.

#### Response:
```json
{
  "home_feed": {
    "Bollywood Songs": [ ... ],
    "Lofi Beats": [ ... ]
  }
}
```

---

## 📁 Project Structure
```
📆 youtube-music-search-api/
│
├── api/index.py                # Main FastAPI application
├── static/favicon.ico     # icon
├── requirements.txt       # Dependencies
└── vercel.json            # Vercel deployment config
```

---

## ⚙️ Deploy to Vercel

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Create `vercel.json`
```json
{
  "builds": [{ "src": "main.py", "use": "@vercel/python" }],
  "routes": [{ "src": "/(.*)", "dest": "main.py" }]
}
```

### 3. Add to `main.py`
```python
from mangum import Mangum
handler = Mangum(app)
```

### 4. Deploy 🚀
```bash
vercel --prod
```

---

## 💡 Future Ideas

- ✅ Redis-based caching
- ✅ Add `/trending` route
- ✅ Playlist or artist-based results
- ✅ Download support or audio stream proxy
- ✅ Language detection from video metadata

---

## 👨‍💻 Author
Built with ❤️ by **[Hrash Vishwakarma]**

---

## 📄 License

```
MIT License

Copyright (c) 2025 Harsh Vishwakarma

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

If you like this project, drop a ⭐ on GitHub or share it!
Have ideas or bugs? Open an issue!

