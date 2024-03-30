from http.client import HTTPResponse
import json
import psycopg2
from fastapi import FastAPI, UploadFile, File, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

app = FastAPI()

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
async def upload_image(image: UploadFile = File(...)):
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO imagess (image_data) VALUES (%s)", (image.file.read(),))
            conn.commit()
            return JSONResponse({"message": "Image uploaded successfully"})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/images")
async def get_images(id: int):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT image_data FROM imagess WHERE id = (%s)", (id,))
            data_memoryview = cursor.fetchone()
            # images = cursor.fetchone()
            # image = images[0]
            # bytesData = bytes(image)
            # for file
            data_bytes = bytes(data_memoryview[0])
            data_bytes.decode('utf-8')
            return Response(data_bytes)
            # for image
            # if bytesData:
            #     return Response(content=bytesData, media_type="image/jpeg")
            # else:
            #     raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
