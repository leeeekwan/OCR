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
from django.core.files.storage import FileSystemStorage
from PIL import Image

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





def task(path,imgname):
    
    #path='./contract5.png'
    files = [('file', open(path,'rb'))]
    src = cv2.imread(os.path.join(path))
    print(src.shape)
    #plt_imshow_bgr(src)
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
 
    char=''
    mon=''
    n=True
    for re in result['images'][0]['fields']:
        if 100<re['boundingPoly']['vertices'][0]['y']<300:
            print(re['boundingPoly']['vertices'][0]['y'])
            char+=re['inferText']
            cv2.rectangle(src, 
                pt1=(300, 270), 
                pt2=(600, 320), 
                color=(0, 0, 255), 
                thickness=5
                )


        if '원' in re['inferText'] and n:
            mon=re['inferText']
            y=int(re['boundingPoly']['vertices'][0]['y'])
            x=int(re['boundingPoly']['vertices'][0]['x'])
            x1=int(re['boundingPoly']['vertices'][2]['x'])
            y1=int(re['boundingPoly']['vertices'][2]['y'])
            cv2.rectangle(src, 
                pt1=(x, y), 
                pt2=(x1, y1), 
                color=(0, 0, 255), 
                thickness=5
                )
            
            src1=cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
            imgfile=Image.fromarray(src1)
            #cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
            imgfile.save(f'./static/imgr/{imgname}.png')
            print(imgname)
            #print(imgfile)
            #imgname= fs.save(f'src-{imgname}', file)
            #imgfile = Image.open(f'./static/imgr/{imgname}')



            n=False
    char=char[-11:-1]

    

    return char,mon



