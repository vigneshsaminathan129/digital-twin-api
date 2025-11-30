from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates folder
templates = Jinja2Templates(directory="templates")

# Google Sheet auth
def fetch_sheet():
    creds = Credentials.from_service_account_file("credentials.json")
    gc = gspread.authorize(creds)
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1Kjo-jfEYdPc_KFoCa4kL_UtBrochTiBLFFYiPQ88lio/edit?usp=sharing")
    ws = sh.worksheet("Copy of No CGM >2D - Vig, Vin")
    data = ws.get_all_values()
    df = pd.DataFrame(data)
    return df

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/coaches")
def get_coaches():
    df = fetch_sheet()
    coaches = sorted(list(set(df[4].tolist()[1:])))
    return {"coaches": coaches}
