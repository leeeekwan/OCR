from django.shortcuts import render
from .models import Employees
from .models import Body
from PIL import Image
from django.core.files.storage import FileSystemStorage

from .ocrtools.resume import naverclova
from .ocrtools.body import title_read


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
            #resulttext = pytesseract.image_to_string(imgfile, lang='kor')
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
            resulttext = title_read(imgfile)
            #지금은 파이테서렉트 쓴것이 리절트 텍스트 
            #은수님의 모듈 결과를 resulttext에 대입해주세요
        context['imgname'] = imgname
        context['resulttext'] = resulttext


    return render(request,'ocrbody.html',context)

# 신체정보 insert 함수
def insertBody(request):
    # 필요한 data = 사원ID, 키, 몸무게, 시력_(좌, 우), 지병
    emp_id = request.POST.get()
    height = request.POST.get('height')
    weight = request.POST.get('weight')
    eye_l = request.POST.get('eye_l')
    eye_r = request.POST.get('eye_r')
    disease = request.POST.get('disease')

    try:
        Body.objects.create(emp=emp_id, height=height, weight=weight, eye_l=eye_l, eye_r=eye_r, disease=disease)
        print('body table에 insert')
    except Exception as e:
        print(e)

    return





