import cv2
import sys
import time
import torch
import socket
import easyocr
import uvicorn
import numpy as np
from loguru import logger
from fastapi import FastAPI, UploadFile, File

logger.add("logs/app2.log", rotation="500 MB")

app = FastAPI()

logger.info(f"{socket.gethostname()} - Downloading model...")
reader = easyocr.Reader(['en'])
logger.info(f"{socket.gethostname()} - Model downloaded")

def recognition(image):
    """

    :param image:
    :return:
    """
    results = []
    texts = reader.readtext(image)
    for (bbox, text, score) in texts:
        xyxy = [int(bbox[0][0]), int(bbox[0][1]), int(bbox[2][0]), int(bbox[2][1])]
        output = {
            "bbox": xyxy,
            "text": text,
            "score": score
        }
        results.append(output)

    return results


@app.post('/ocr')
async def predict(imagefile: UploadFile = File(...)):
    """
    received request from client and process the image
    :return: dict of width and points
    """
    try:
        start = time.time()
        logger.info(f"{socket.gethostname()} - Request received")
        image_data = await imagefile.read()
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_UNCHANGED)
        results = recognition(image)
        time_taken = time.time() - start
        logger.info(f"{socket.gethostname()} - Request processed in {time_taken:.4f} seconds")

        return {
            "container_ID": socket.gethostname(),
            "using_gpu": torch.cuda.is_available(),
            "results": results
        }
    except:
        logger.error(f"{socket.gethostname()} - Error processing request")
        return {"error": "Error processing request"}

@app.get('/test')
async def predict():
    logger.info(f"{socket.gethostname()} - Request received")
    results = 1/0
    
    return {
        "container_ID": socket.gethostname(),
        "using_gpu": torch.cuda.is_available(),
        "results": results
    }

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)

