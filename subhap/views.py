from django.shortcuts import render
from .models import Employees
from PIL import Image
from django.core.files.storage import FileSystemStorage
import pytesseract
from .ocrtools.resume import naverclova

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
def ocrarmy(request):
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
            resulttext = pytesseract.image_to_string(imgfile, lang='kor')
            #지금은 파이테서렉트 쓴것이 리절트 텍스트 
            #종성님의 모듈 결과를 resulttext에 대입해주세요
        context['imgname'] = imgname
        context['resulttext'] = resulttext


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
            resulttext = pytesseract.image_to_string(imgfile, lang='kor')
            #지금은 파이테서렉트 쓴것이 리절트 텍스트 
            #은수님의 모듈 결과를 resulttext에 대입해주세요
        context['imgname'] = imgname
        context['resulttext'] = resulttext


    return render(request,'ocrbody.html',context)
