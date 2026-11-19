from contextlib import asynccontextmanager
from datetime import date
from typing import Literal

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import get_connection, initialize_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(title="교내 분실물 관리 서비스", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


def fetch_items(status: str | None = None):
    query = "SELECT * FROM found_items"
    parameters: tuple[str, ...] = ()
    if status in {"보관 중", "전달 완료"}:
        query += " WHERE status = ?"
        parameters = (status,)
    query += " ORDER BY created_at DESC, id DESC"
    with get_connection() as connection:
        return connection.execute(query, parameters).fetchall()


@app.get("/")
def home(request: Request, status: str | None = None):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"items": fetch_items(status), "selected_status": status},
    )


@app.get("/items/new")
def new_item_form(request: Request):
    return templates.TemplateResponse(request, "new_item.html", {"today": date.today().isoformat()})


@app.post("/items")
def create_item(
    name: str = Form(...),
    category: str = Form(...),
    found_location: str = Form(...),
    found_date: str = Form(...),
    storage_location: str = Form(...),
    description: str = Form(""),
):
    with get_connection() as connection:
        connection.execute(
            """INSERT INTO found_items
            (name, category, found_location, found_date, storage_location, description)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (name.strip(), category, found_location.strip(), found_date, storage_location.strip(), description.strip()),
        )
    return RedirectResponse(url="/", status_code=303)


@app.get("/items/{item_id}")
def item_detail(request: Request, item_id: int):
    with get_connection() as connection:
        item = connection.execute("SELECT * FROM found_items WHERE id = ?", (item_id,)).fetchone()
    if item is None:
        raise HTTPException(status_code=404, detail="분실물을 찾을 수 없습니다.")
    return templates.TemplateResponse(request, "item_detail.html", {"item": item})


@app.post("/items/{item_id}/status")
def update_status(item_id: int, status: Literal["보관 중", "전달 완료"] = Form(...)):
    with get_connection() as connection:
        result = connection.execute("UPDATE found_items SET status = ? WHERE id = ?", (status, item_id))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="분실물을 찾을 수 없습니다.")
    return RedirectResponse(url=f"/items/{item_id}", status_code=303)

