from django.shortcuts import render
from PIL import Image
from django.core.files.storage import FileSystemStorage
import pytesseract
# Create your views here.

def upload(request):
    context={}


    return render(request, 'upload.html',context)

def ocr(request):
    print('ocr')
    context = {}
    context['menutitle'] = 'OCR READ'
    
    imgname = ''
    resulttext = ''
    print(request.FILES)
    if 'uploadfile' in request.FILES:
        print(100)
        uploadfile = request.FILES.get('uploadfile', '')
            
        if uploadfile != '':
            name_old = uploadfile.name
            print(name_old)
            print('sdfsdf')
            fs = FileSystemStorage(location = 'static/source')
            imgname= fs.save(f'src-{name_old}', uploadfile)
            print(imgname)
            imgfile = Image.open(f'./static/source/{imgname}')
            resulttext = pytesseract.image_to_string(imgfile, lang='kor')

        context['imgname'] = imgname
        context['resulttext'] = resulttext.replace(" ", "")
        print(resulttext)

    return render(request,'ocr.html',context)
