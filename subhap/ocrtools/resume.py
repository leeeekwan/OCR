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

def naverclova(path):
    resulttext=[]
    # img=np.array(img)
    # img=io.BytesIO(img)
    files1=[('file',open(path,'rb'))]
    #src3 = cv2.imread(fy)
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


    #우리가 보내는것은 리쿼스트 그리고 그 유알엘이 우리한테 주는건 리스판스
    response1=requests.request("POST",api_url,headers=headers,data=payload, files=files1)
    #response = requests.request("POST", api_url, headers=headers, data=payload, files=files)

    #result = response.json()
    result1=response1.json()
    # for i in result['images'][0]['fields']:
    #     if i['inferText']=='인턴·대외활동':
    #         #print(i['inferText'])
    #         pt11=int(i['boundingPoly']['vertices'][0]['x'])
    #         bot=int(i['boundingPoly']['vertices'][0]['y'])
    #         print(i)
    #         pt21=int(i['boundingPoly']['vertices'][2]['x'])
    #         pt22=int(i['boundingPoly']['vertices'][2]['y'])
    #     if i['inferText']=='학력':
    #         #print(i['inferText'])
    #         pt11=int(i['boundingPoly']['vertices'][0]['x'])
    #         pt12=int(i['boundingPoly']['vertices'][0]['y'])
    #         print(i)
    #         pt21=int(i['boundingPoly']['vertices'][2]['x'])
    #         up=int(i['boundingPoly']['vertices'][2]['y'])
    # print(up)
    # print(bot)
    # ch=''
    # for i in result['images'][0]['fields']:
    #     if up<int(i['boundingPoly']['vertices'][0]['y'])<bot:
    #         ch+=i['inferText']
    #     if '대학교' in  i['inferText']:
    #         uni=i['inferText']
    #         print(uni)
    # #cv2.rectangle(src3, pt1=(pt11,pt12), pt2=(pt21,pt22),color=(255,0,0), thickness=2)
    # #   cv2.rectangle(src3, pt1=(pt11,pt12), pt2=(pt21,pt22),color=(255,0,0), thickness=2)
    # #plt_imshow_bgr(src3)
    #     if i['inferText'] == '학력':
    #         st=i['boundingPoly']['vertices'][0]['y']
    #         print(st)
    # char=''
    # for i in result['images'][0]['fields']:
    #     if bot < i['boundingPoly']['vertices'][0]['y']< st:
            
    #             char+=i['inferText']
    #             char+=' '
                
    # print(char)
    


    for i in result1['images'][0]['fields']:
        
    
        if i['inferText']=='자격증':
            up=i['boundingPoly']['vertices'][3]['y']
        
        
        if i['inferText']=='자기소개서':
            
            bot=i['boundingPoly']['vertices'][0]['y']
            

    ja=''
    for i in result1['images'][0]['fields']:
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
            




        



