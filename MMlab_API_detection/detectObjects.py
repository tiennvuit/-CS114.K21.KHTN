import base64
import urllib.parse
import requests
import json
import sys
import argparse
from user_login import get_token
import time
from PIL import Image

url = 'http://service.mmlab.uit.edu.vn/mmlab_api/object_detect'


def get_boundingBoxes(image_path: str):
    """
    Input: 

    Output: json file that store informations of objects in image.
    """
    # Get token from API Mmlab.
    token = get_token()
    image = open(image_path, 'rb')
    image_read = image.read()
    encoded = base64.encodebytes(image_read)
    encoded_string = encoded.decode('utf-8')
    data = {
        'api_version': '1.0',
        'data': {
            'method': 'yolov3',
            'model_id': '1575949128.9343169',
            'images': [encoded_string, encoded_string]
        }
    }
    headers = {'Content-type': 'application/json', 'Authorization': "bearer " + token}
    data_json = json.dumps(data)
    response = requests.post(url, data = data_json, headers=headers)
    return response.json()


def draw_bounding_boxes(image, bboxes: json):
    bboxes = bboxes["data"]["predicts"][0] +  bboxes["data"]["predicts"][1]
    


def main(args):
    image_path = str(args.path)
    # Get bouding boxes of objects in image.
    bboxes = get_boundingBoxes(image_path=image_path)
    print(bboxes)
    # Draw bounding boxes to image.
    # draw_bounding_boxes(image=image, bboxes=bboxes)
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The program using API of Mmlab-UIT to detect multiable object")
    parser.add_argument("--path", help="The path of image", default="test.png")
    args = parser.parse_args()
    main(args)
    