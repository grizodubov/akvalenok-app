from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.spaces.router import get_spaces_by_location_and_time

router = APIRouter(prefix="/pages", tags=["Фронтенд"])


templates = Jinja2Templates(directory="app/templates")


@router.get("/spaces", response_class=HTMLResponse)
async def get_spaces_page(
        request: Request, spaces=Depends(get_spaces_by_location_and_time)
):
    return templates.TemplateResponse(
        name="spaces.html",
        context={"request": request, "spaces": spaces},
    )
