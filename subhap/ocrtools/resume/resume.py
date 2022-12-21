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
import io
from PIL import Image

#네이버 클로바
base_path = r'.'

def cv2_imshow(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def plt_imshow_bgr(bgr_img):
    cvtImg = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    plt.imshow(cvtImg)
    plt.show()



# fy=os.path.join(base_path,'minsu.png')
# path='./minsu.png'
# files = [('file', open(path,'rb'))]

# path1='./minsu2.png'
#flowers/subhap/ocrtools/res10_300x300_ssd_iter_140000_fp16.caffemodel
#flowers/subhap/ocrtools/deploy.prototxt.txt

def facedetect(path,k):
    print(k,'oipoipoi')
    frame=cv2.imread(path)
    model = os.path.join('/Users/general/Documents/flower/flowers/subhap/ocrtools/resume/res10_300x300_ssd_iter_140000_fp16.caffemodel')
    config = os.path.join('/Users/general/Documents/flower/flowers/subhap/ocrtools/resume/dproto.txt')
    print(model,config)
    print('봐봐 시발 이게 안되잔아')
    net = cv2.dnn.readNet(model, config)
    blob=cv2.dnn.blobFromImage(frame,1,(300,300),(104,177,123))
    net.setInput(blob)
    detect=net.forward()
    print(detect.shape)
    detect =detect[0,0,:,:]
    print(detect[0])
    (h,w)=frame.shape[:2]
    for i in range(detect.shape[0]):
        confidence=detect[i,2]
        
        if confidence <0.5: 
            break
        x1 = int(detect[i, 3] * w)
        y1 = int(detect[i, 4] * h)
        x2 = int(detect[i, 5] * w)
        y2 = int(detect[i, 6] * h)
    cx=(x2+x1)/2
    cy=(y2+y1)/2
    img_cropped = cv2.getRectSubPix(
            frame, 
            patchSize=(100,120), 
            center=(cx,cy)
        )
    cvtImg = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB)
    a=Image.fromarray(cvtImg)
    a.save(f'./static/face/{k}.png')

def naverclova(path,path1):
    resulttext=[]
    files=[('file',open(path,'rb'))]
    files1=[('file',open(path1,'rb'))]
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


    #우리가 보내는것은 리쿼스트 그리고 그 유알엘이 우리한테 주는건 리스판스
    response1=requests.request("POST",api_url,headers=headers,data=payload, files=files1)
    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)

    result = response.json() #minsu2
    result1=response1.json()
   
    for i in result1['images'][0]['fields']:
        if i['inferText']=='인턴·대외활동':
            print('인턴 대외 활동')
            pt11=int(i['boundingPoly']['vertices'][0]['x'])
            bot=int(i['boundingPoly']['vertices'][0]['y'])
            
            pt21=int(i['boundingPoly']['vertices'][2]['x'])
            pt22=int(i['boundingPoly']['vertices'][2]['y'])
        if i['inferText']=='학력':
            print('학력')
            pt11=int(i['boundingPoly']['vertices'][0]['x'])
            pt12=int(i['boundingPoly']['vertices'][0]['y'])
            print(i)
            pt21=int(i['boundingPoly']['vertices'][2]['x'])
            up=int(i['boundingPoly']['vertices'][2]['y'])
    print(up)
    print(bot)
    ch=''
    for i in result1['images'][0]['fields']:
        if up<int(i['boundingPoly']['vertices'][0]['y'])<bot:
            ch+=i['inferText']
   
        if '대학교' in  i['inferText']:
            uni=i['inferText']
            #print(uni)
    #cv2.rectangle(src3, pt1=(pt11,pt12), pt2=(pt21,pt22),color=(255,0,0), thickness=2)
    #   cv2.rectangle(src3, pt1=(pt11,pt12), pt2=(pt21,pt22),color=(255,0,0), thickness=2)
    #plt_imshow_bgr(src3)
        if i['inferText'] == '학력':
            st=i['boundingPoly']['vertices'][0]['y']
            #print(st)

    print(ch,'ch')
    
    resulttext.append(ch)          
   
    


    for i in result['images'][0]['fields']:
        
    
        if i['inferText']=='자격증':
            up=i['boundingPoly']['vertices'][3]['y']
        
        
        if i['inferText']=='자기소개서':
            
            bot=i['boundingPoly']['vertices'][0]['y']
            

    ja=''
    for i in result['images'][0]['fields']:
        if up<i['boundingPoly']['vertices'][0]['y']<bot:
        
            
            if '.' in i['inferText'] or i['inferText'].isnumeric():
                i['inferText']=''
                ja+='/'

            ja+=i['inferText']
    a=ja.split('/')
    for s in a:
        if s!='':
            resulttext.append(s)

    return resulttext
            




        



