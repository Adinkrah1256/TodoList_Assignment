
# Todo-list-Assignment

## Prerequisites
- Python 3.14+ installed (see `requires-python` in `backend/pyproject.toml`)
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed
- A modern web browser

## How to Run the Project

> **Note:** Start the backend first, since the frontend makes API calls to it.

### 1. Start the Backend
The backend is built with Python (FastAPI) and uses `uv` for dependency management.

1. Open your terminal and navigate to the backend folder:
```bash
cd backend
```

2. Install the required dependencies:
```bash
uv sync
```

3. Start the development server:
```bash
uv run fastapi dev main.py
```

   (The API will typically be available at http://127.0.0.1:8000)

This project's `pyproject.toml` already includes `fastapi[standard]`, so the `fastapi dev` command works out of the box, and `main.py` already defines `app = FastAPI()` with `CORSMiddleware` enabled.

> **Note on CORS config:** `main.py` currently sets `allow_origins=["*"]` together with `allow_credentials=True`. Per the CORS spec, a wildcard origin cannot be combined with credentialed requests — this works fine for the current app (no cookies/auth, plain `fetch()` calls), but if you add authentication later, switch to an explicit list of allowed origins instead of `"*"`.

### 2. Start the Frontend
The frontend consists of standard web files (HTML, CSS, JS).

1. Open a new terminal window or file explorer and navigate to the `frontend` folder.
2. Open the `index.html` file directly in your web browser. (Alternatively, use an extension like VS Code Live Server to serve the file dynamically).

> **Note:** Opening `index.html` directly (`file://`) sends `Origin: null` on API requests. If you see CORS errors in the browser console, confirm the backend's `CORSMiddleware` allows this origin, or serve the frontend via Live Server instead.
