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

g_df =pd.DataFrame()
file_uploaded =""
@app.post("/uploadfiles", response_class=HTMLResponse)
async def uploadfiles(request: Request, files: UploadFile = Form("individual"), column_select: str = Form(" ")):
    global g_df
    global file_uploaded
    if files =="individual":
        f_df = g_df
    else:
        df =pd.read_csv(files.file)
        g_df =df
        f_df= g_df
        file_uploaded = files.filename
    lst = f_df.columns.to_list()
    col_dtypes =[cols+'('+str(f_df.dtypes[cols]) +')' for cols in lst]
    #f_df.columns=col_dtypes
    if column_select !=" ":
        unique_list =f_df[column_select].unique()
    else:
        unique_list=''
        
    return templates.TemplateResponse(
        "form.html",
        {
            "request": request,
            "tab": f_df.head(2).to_html(border=1, index=False,table_id="table_details"),
            "Res": file_uploaded,
            "col_list": lst,
            "col_sel": column_select,
            "final_res": unique_list
        },
    )


# main
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
