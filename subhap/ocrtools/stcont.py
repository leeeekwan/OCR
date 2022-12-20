import os
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')
import uuid
import time
import requests
import json


base_path = r'.'
show=os.path.join(base_path,'contract.png')

def cv2_imshow(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def plt_imshow_bgr(bgr_img):
    cvtImg = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    plt.imshow(cvtImg)
    plt.show()
def task(path):
    
    #path='./contract5.png'
    files = [('file', open(path,'rb'))]
    #src3 = cv2.imread(show)
    #print(src3.shape)
    #print(type(plt_imshow_bgr(src3)))
    #print(type(src3))
    api_url = 'https://byoawp590b.apigw.ntruss.com/custom/v1/19592/c2e2067f630cd03dc609abedf56e14f81826e57380d0f5c33daec73fb634b1a7/general'
    secret_key = 'R0lwV2NjTlVCbWlvRHBlQWVSQmxtSlBSZldHc1BIS0I='
    request_json = {'images': [{'format': 'jpg',
                                    'name': 'demo'
                                }],
                        'requestId': str(uuid.uuid4()),
                        'version': 'V2',
                        'timestamp': int(round(time.time() * 1000))
                    }
    
    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    
    headers = {
    'X-OCR-SECRET': secret_key,
    }

    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    result = response.json()
    #plt_imshow_bgr(src3)
    char=''
    mon=''
    n=True
    for re in result['images'][0]['fields']:
        if 100<re['boundingPoly']['vertices'][0]['y']<300:
            char+=re['inferText']
        if '원' in re['inferText'] and n:
            mon=re['inferText']
            n=False
    char=char[-11:-1]

    

    return char,mon



