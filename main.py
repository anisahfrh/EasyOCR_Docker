import cv2
import easyocr
import uvicorn
import numpy as np
from fastapi import FastAPI, UploadFile, File

reader = easyocr.Reader(['en'])

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
    image_data = await imagefile.read()
    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_UNCHANGED)
    results = recognition(image)

    return {
        "results": results
    }

if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)

