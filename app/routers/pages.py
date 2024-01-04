from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/login")
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/signup")
async def root(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.get("/account")
async def root(request: Request):
    return templates.TemplateResponse("account.html", {"request": request})