from fastapi import FastAPI, Form, Request
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import shutil
import pandas as pd

# initialization
app = FastAPI()

# mount static folder to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 template instance for returning webpage via template engine
templates = Jinja2Templates(directory="templates")

# serve webpage, GET method, return HTML
@app.get("/", response_class=HTMLResponse)
async def get_webpage(request: Request):
    return templates.TemplateResponse(
        "form.html", {"request": request, "Res": "Please upload a csv file"}
    )


@app.post("/uploadfiles", response_class=HTMLResponse)
async def uploadfiles(request: Request, files: UploadFile = Form(...)):
    with open("destination.csv", "wb") as buffer:
        shutil.copyfileobj(files.file, buffer)
    df =pd.read_csv("destination.csv")
        
    return templates.TemplateResponse(
        "form.html", {"request": request, "tab": df.head(5).to_html(border =1,index=False,show_dimensions =True),"Res" :files.filename}
    )


# main
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
