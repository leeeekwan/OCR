import os
import sys
import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageFont, Image, ImageDraw
plt.style.use('seaborn-white')

#base_path = r'C:\Users\gram\Desktop\project_3'

# def plt_imshow(bgr_img):
#     cvtImg = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
#     plt.figure(figsize=(30, 15))
#     plt.imshow(cvtImg)
#     plt.show()


# # 이미지 읽어오기
# body1 = cv2.imread(os.path.join(base_path, 'body4.jpg'))
# body1_re = cv2.resize(body1, (0, 0), fx = 2, fy = 2)

# body2 = cv2.imread(os.path.join(base_path, 'body5.jpg'))
# body2_re = cv2.resize(body2, (0, 0), fx = 2, fy = 2)

# body3 = cv2.imread(os.path.join(base_path, 'body6.jpg'))
# body3_re = cv2.resize(body3, (0, 0), fx = 2, fy = 2)


def three_img(img1, img2, img3):
    cvtImg1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    cvtImg2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    cvtImg3 = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)
    
    plt.figure(figsize=(15, 7))
    plt.subplot(131), plt.imshow(cvtImg1)
    plt.subplot(132), plt.imshow(cvtImg2)
    plt.subplot(133), plt.imshow(cvtImg3)
    plt.show()

xy_data = {
    'firstX' : (700, 1500),
    'firstY' : (2400, 2500),
    'secondX' : (320, 1900),
    'secondY' : (465, 900),
    'thirdX' : (300, 1800),
    'thirdY' : (1550, 1950)
          }


def title_read(img):
    resulttext = {'date' : ''}   # date, disease, height, weight, eye_L, eye_R

    img=np.array(img)
    img = cv2.resize(img, (0, 0), fx = 2, fy = 2)

    x = (250, 1500)
    y = (300, 500)
    
    reader = easyocr.Reader(['ko'], gpu=False)
    title = reader.readtext(img[y[0]:y[1], x[0]:x[1]])
    
    
    for ti in title:
        if "심뇌혈관질환" in ti[1]:   # 날짜
            print(f'{ti[1]} body1')
            
            result = reader.readtext(img[
                xy_data['firstY'][0]:xy_data['firstY'][1],
                xy_data['firstX'][0]:xy_data['firstX'][1]
            ])
            
            for dt in result:
                resulttext['date'] += dt[1]

            print(resulttext['date'])
                        
                
            break
        
        elif "건강검진" in ti[1]:   # 유질환
            print(f'{ti[1]} body3')
            
            result = reader.readtext(img[
                xy_data['thirdY'][0]:xy_data['thirdY'][1],
                xy_data['thirdX'][0]:xy_data['thirdX'][1]
            ])
            
            for i in range(len(result)):
                if result[i][1] == "유질환":
                    resulttext['disease'] = result[i + 1][1]
                    
                    print(resulttext['disease'])
            
            break
        
        else:               # 키, 몸무게, 청력, 시력
            print(f'{ti[1]} body2')
            
            result = reader.readtext(img[
                xy_data['secondY'][0]:xy_data['secondY'][1],
                xy_data['secondX'][0]:xy_data['secondX'][1]
            ])
                
            for i in range(len(result)):
                if "및 몸무게" in result[i][1]:
                    resulttext['height'] = result[i + 1][1]
                    resulttext['weight'] = result[i + 2][1]
                
                    print(resulttext['height'], resulttext['height'])
                
                if '시력' in result[i][1]:
                    resulttext['eye_l'] = result[i + 1][1]
                    resulttext['eye_r'] = result[i + 2][1]
                
                    print(resulttext['eye_l'], resulttext['eye_r'])
            
            break

    return resulttext







