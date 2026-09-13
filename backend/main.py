from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.routers.auth import router as auth_router
from backend.routers.groups import router as groups_router
from backend.routers.chat import router as chat_router
from backend.routers.events import router as events_router
from backend.routers.polls import router as polls_router
from backend.routers.expenses import router as expenses_router
from backend.routers.group_membership import router as membership_router
from backend.routers.tasks import router as tasks_router
from backend.routers.food import router as food_router
from backend.routers.gallery import router as gallery_router
from backend.routers.notifications import router as notifications_router


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


app = FastAPI(
    title="GatherUp API",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(groups_router)
app.include_router(chat_router)
app.include_router(events_router)
app.include_router(polls_router)
app.include_router(expenses_router)
app.include_router(membership_router)
app.include_router(tasks_router)
app.include_router(food_router)
app.include_router(gallery_router)
app.include_router(notifications_router)


app.mount(
    "/assets",
    StaticFiles(directory=FRONTEND_DIR),
    name="assets"
)


@app.get("/", include_in_schema=False)
def root():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/login", include_in_schema=False)
def login_page():
    return FileResponse(FRONTEND_DIR / "login.html")


@app.get("/register", include_in_schema=False)
def register_page():
    return FileResponse(FRONTEND_DIR / "register.html")


@app.get("/dashboard", include_in_schema=False)
def dashboard_page():
    return FileResponse(FRONTEND_DIR / "dashboard.html")


@app.get("/verify-email", include_in_schema=False)
def verify_email_page():
    return FileResponse(FRONTEND_DIR / "verify-email.html")


@app.get("/service-worker.js", include_in_schema=False)
def service_worker():
    return FileResponse(
        FRONTEND_DIR / "service-worker.js",
        media_type="application/javascript"
    )


@app.get("/group", include_in_schema=False)
def group_page():
    return FileResponse(FRONTEND_DIR / "group.html")