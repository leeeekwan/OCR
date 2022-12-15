from django.shortcuts import render
from .models import Employees
from PIL import Image
from django.core.files.storage import FileSystemStorage
import pytesseract
from .ocrtools.resume import naverclova


#------------------------------------------------------
# 병역문서 인식을 위해 필요한 import 들
from easyocr.easyocr import *
import cv2
import requests
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import os


import sys

import matplotlib.pyplot as plt
plt.style.use('seaborn-white')

from .ocrtools.armyOCR.easy.army import call_army
# -------------------------------------------------
# Create your views here.

def home(request):

    employees = Employees.objects.all()

    context = {
        'employees' : employees,
    }

    return render(request, 'index.html', context)



def result(request,i):
    emp= Employees.objects.get(id=i)
    context={
        'name':emp.name,
        

    }


    return render(request, 'result.html',context)

def ocr(request):
    print('ocr')
    context = {}
    context['menutitle'] = 'OCR READ'
    
    imgname = ''
    resulttext = ''
    
    if 'uploadfile' in request.FILES:
        print(100)
        uploadfile = request.FILES.get('uploadfile', '')
            
        if uploadfile != '':
            name_old = uploadfile.name
            
            fs = FileSystemStorage(location = 'static/source')
            imgname= fs.save(f'src-{name_old}', uploadfile)
            print(imgname)
            imgfile = Image.open(f'./static/source/{imgname}')
            path=f'./static/source/{imgname}'
            
            resulttext=naverclova(path)
        context['imgname'] = imgname
        context['resulttext'] = resulttext
        
    

    return render(request,'ocr.html',context)





# -------------------------------------------------------------------------------

# 병역문서 불러오는 부분

def ocrarmy(request):
    context = {}
    if 'uploadfile' in request.FILES:
        
        
        # uploadfile은 html에서 불러오는 것
        uploadfile = request.FILES.get('uploadfile', '')
            
        if uploadfile != '':
            name_old = uploadfile.name


            # 이미지를 불러오는 경로도 좀 손을 봐야 한다
            

            fs = FileSystemStorage(location = 'static\source\document_army')    # 이미지들이 저장되는 곳
            imgname= fs.save(f'src-{name_old}', uploadfile)       # 이미지를 저정하는 동작 (이미지명, 이미지파일)
            # print(imgname)                                        # 이미지명 확인


            path=f'static\source\document_army'                   # 이미지를 불러올 경로



            # ------------------------------------------------- 
            # 만들어둔 EasyOCR을 부르는 부분
            # subhap\ocrtools\armyOCR\easy 경로에서 army.py 에서 call_army를 호출 경로를 보내줌

            resulttext = call_army(path)    
            # resulttext = call_army(path, imgname)   
            context['resulttext']=resulttext 
            context['imgname']=imgname

            # ---------------------------------------------------

    return render(request,'ocrarmy.html',context)




def ocrbody(request):
    context = {}
    if 'uploadfile' in request.FILES:
        
        uploadfile = request.FILES.get('uploadfile', '')
            
        if uploadfile != '':
            name_old = uploadfile.name
            
            fs = FileSystemStorage(location = 'static/source')
            imgname= fs.save(f'src-{name_old}', uploadfile)
            print(imgname)
            imgfile = Image.open(f'./static/source/{imgname}')
            path=f'./static/source/{imgname}'
            #resulttext = pytesseract.image_to_string(imgfile, lang='kor')
            #지금은 파이테서렉트 쓴것이 리절트 텍스트 
            #은수님의 모듈 결과를 resulttext에 대입해주세요
        resulttext='' 
        context['imgname'] = imgname
        context['resulttext'] = resulttext


    return render(request,'ocrbody.html',context)

