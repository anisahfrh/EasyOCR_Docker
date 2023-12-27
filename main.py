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

reader = easyocr.Reader(['en'])
logger.add("logs/app.log", rotation="500 MB")

app = FastAPI()

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
        logger.info(f"Request received by container ID: {socket.gethostname()}")
        image_data = await imagefile.read()
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_UNCHANGED)
        results = recognition(image)
        time_taken = time.time() - start
        logger.info(f"Request processed in {time_taken:.4f} seconds")

        return {
            "container_ID": socket.gethostname(),
            "using_gpu": torch.cuda.is_available(),
            "results": results
        }
    except:
        logger.error(f"Error processing request: {str(e)}")
        return {"error": str(e)}

if __name__=="__main__":
    logger.add(sys.stdout, level="INFO", format="<green>{time}</green> <level>{message}</level>")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)

