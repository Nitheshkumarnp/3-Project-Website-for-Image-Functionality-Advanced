from http.client import HTTPResponse
import json
import psycopg2
from fastapi import FastAPI, UploadFile, File, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import logging

app = FastAPI()
logger = logging.getLogger()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
# Database connection
conn = psycopg2.connect(
    host=os.getenv("host"),
    port=os.getenv("port"),
    database=os.getenv("database"),
    user=os.getenv("user"),
    password=os.getenv("password")
)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        with conn.cursor() as cursor:
            logger.warning('This is a warning message : ', file)
            logger.error('This is an error message : ', file)
            logger.critical('This is a critical message : ', file)
            file_name, file_extension = os.path.splitext(file.filename)
            logger.warning('This is a warning message : ', file_name, file_extension)
            logger.error('This is an error message : ', file_name, file_extension)
            logger.critical('This is a critical message : ', file_name, file_extension)
            file_content = await file.read()
            cursor.execute("INSERT INTO files (name, extension, content) VALUES (%s, %s, %s)", (file_name, file_extension, file_content))
            conn.commit()
            return JSONResponse({"message": "Image uploaded successfully"})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/list")
async def get_all_details():
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name, extension FROM files")
            rows = cursor.fetchall()
            file_list = []
            for row in rows:
              file_list.append(row[0] + row[1])
            return JSONResponse({"fileList": file_list})
            #return file_list
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/file")
async def get_all_details(file_name_with_extension: str):
    try:
        with conn.cursor() as cursor:
            file_name, file_extension = os.path.splitext(file_name_with_extension)
            cursor.execute('SELECT * FROM files where name = (%s) and extension = (%s)', (file_name, file_extension,))
            rows = cursor.fetchone()
            name, extension, content = rows
            byte_data = bytes(content)
            if extension == '.txt':
              decoded = byte_data.decode("utf-8")
              return Response(decoded, media_type="text/plain") 
            elif(extension == '.jpeg' or extension == '.png'):
              # return byte_data
              return Response(content=byte_data, media_type="image/jpeg")
            else:
                raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
