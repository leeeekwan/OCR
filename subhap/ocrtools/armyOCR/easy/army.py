from easyocr.easyocr import *

# -------------------
import cv2
import requests
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import os


import sys

import matplotlib.pyplot as plt
plt.style.use('seaborn-white')
# ---------------------



# GPU 설정
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'


def get_files(path):
    file_list = []

    files = [f for f in os.listdir(path) if not f.startswith('.')]  # skip hidden file
    files.sort()
    abspath = os.path.abspath(path)
    for file in files:
        file_path = os.path.join(abspath, file)
        file_list.append(file_path)

    return file_list, len(file_list)



def call_army(path):
    print('잘들어감')
# def call_army(path, imgname):


    # Using custom model
    # 기존 GPU True 이던 것을 False로 바꿈

    # 실질적인 OCR 작동을 불러오는 부분, 커스텀 모델의 적용등이 여기서 이루어짐
    reader = Reader(['ko'], gpu=False,
                    # model_storage_directory='./workspace/user_network_dir',
                    #model_storage_directory=r'subhap\ocrtools\armyOCR\easy\workspace\user_network_dir',
                    model_storage_directory=r'subhap/ocrtools/armyOCR/easy/workspace/user_network_dir',
                    # user_network_directory='./workspace/user_network_dir',
                    #user_network_directory=r'subhap\ocrtools\armyOCR\easy\workspace\user_network_dir',
                    user_network_directory=r'subhap/ocrtools/armyOCR/easy/workspace/user_network_dir',
                    recog_network='custom')

    # 폴더 안의 이미지를 상단부터 하단 순으로 순차적으로 불러옴
    files, count = get_files(path)   # 이미지를 불러오는 경로
    # file = cv2.imread(os.path.join(path, imgname))

  

# -------------------------------------------------------


    # 불러온 이미지들을 반복문을 이용하여 순서대로 불러옴
    # 이미지를 폴더를 지정, 폴더 내부의 것을 순차적으로 불러옴 ---------------------------------------------
    for idx, file in enumerate(files):
        filename = os.path.basename(file)



        result = reader.readtext(file, # paragraph=True, 
                                decoder='wordbeamsearch',   # wordbeamsearch
                                contrast_ths=0.4,           # contrast_ths : 정확도 0.5 인 텍스트 모델에 다시 돌리는 것
                                adjust_contrast=0.6,
                                canvas_size  = 1260,        # 1260 (예비역, 만기)
                                mag_ratio = 7,              # 확대 정도
                                beamWidth  = 10
                                )
        



        # ./easyocr/utils.py 733 lines
        # result[0]: bbox
        # result[1]: string
        # result[2]: confidence

        count = 0
        a_info = {'군별': None,'계급': None,'군번': None,'역중':None,'병과':None,'입영일':None,'전역일': None,'전역':None}

        for (bbox, string, confidence) in result:
        # for (bbox, string) in result:

            if string == '군별':
                count += 1

            if count >= 1:
                if count % 2 ==0:
                    print(string)
                    if count//2 == 1:
                        a_info['군별']=string
                    if count//2 == 2:
                        a_info['계급']=string
                    if count//2 == 3:
                        a_info['군번']=string
                    if count//2 == 4:
                        a_info['역중']=string
                    if count//2 == 5:
                        a_info['병과']=string
                    if count//2 == 6:
                        a_info['입영일']=string
                    if count//2 == 7:
                        a_info['전역일']=string
                    if count//2 == 8:
                        a_info['전역']=string

                if string == '만기':
                    break
                count += 1
            
        # print(a_info)

        a_text = "군별 : "+a_info['군별']+"\n"+"계급 : "+a_info['계급']+"\n"+"군번 : "+a_info['군번']+"\n"+"역중 : "+a_info['역중']+"\n"+"병과 : "+a_info['병과']+"\n"+"입영일 : "+a_info['입영일']+"\n"+"전역일 : "+a_info['전역일']+"\n"+"전역사유 : "+a_info['전역']

        return a_text


# 이미지를 1개만 불러오는 경우 ----------------------------------------------

    
    



    # result = reader.readtext(file, # paragraph=True, 
    #                         decoder='wordbeamsearch',   # wordbeamsearch
    #                         contrast_ths=0.4,           # contrast_ths : 정확도 0.5 인 텍스트 모델에 다시 돌리는 것
    #                         adjust_contrast=0.6,
    #                         canvas_size  = 1260,        # 1260 예비역, 만기
    #                         mag_ratio = 7,              # 확대 정도
    #                         beamWidth  = 10
    #                         )
    



    # # ./easyocr/utils.py 733 lines
    # # result[0]: bbox
    # # result[1]: string
    # # result[2]: confidence

    # count = 0
    # a_info = {'군별': None,'계급': None,'군번': None,'역중':None,'병과':None,'입영일':None,'전역일': None,'전역':None}

    # for (bbox, string, confidence) in result:
    # # for (bbox, string) in result:

    #     if string == '군별':
    #         count += 1

    #     if count >= 1:
    #         if count % 2 ==0:
    #             print(string)
    #             if count//2 == 1:
    #                 a_info['군별']=string
    #             if count//2 == 2:
    #                 a_info['계급']=string
    #             if count//2 == 3:
    #                 a_info['군번']=string
    #             if count//2 == 4:
    #                 a_info['역중']=string
    #             if count//2 == 5:
    #                 a_info['병과']=string
    #             if count//2 == 6:
    #                 a_info['입영일']=string
    #             if count//2 == 7:
    #                 a_info['전역일']=string
    #             if count//2 == 8:
    #                 a_info['전역']=string

    #         if string == '만기':
    #             break
    #         count += 1
        
    # # print(a_info)

    # a_text = "군별 : "+a_info['군별']+"\n"+"계급 : "+a_info['계급']+"\n"+"군번 : "+a_info['군번']+"\n"+"역중 : "+a_info['역중']+"\n"+"병과 : "+a_info['병과']+"\n"+"입영일 : "+a_info['입영일']+"\n"+"전역일 : "+a_info['전역일']+"\n"+"전역사유 : "+a_info['전역']

    # return a_text