from django.shortcuts import render, redirect
from .models import Employees, Body, Info, Soldier
from PIL import Image
from django.core.files.storage import FileSystemStorage
from .ocrtools.resume.resume import naverclova,facedetect
from .ocrtools.body import title_read
from .ocrtools.resident import resident
from .ocrtools.stcont import task

from django.shortcuts import redirect



#------------------------------------------------------
# 병역문서 인식을 위해 필요한 import 들
from easyocr.easyocr import *
import numpy as np
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
    print(111)

    msg = "정보를 불러올 수 없습니다."
 
    emp= Employees.objects.get(id=i)

    context = {
        'name':emp.name,
        'idx':i,
        'class_field':emp.class_field,
    }

    try:
        employees = Employees.objects.get(id = i)
        context['employees'] = employees

    except Exception as e:

        context['msg'] = msg

    try:
        body = Body.objects.get(emp = i)
        context['body'] = body

    except Exception as e:

        context['msg'] = msg

    try:
        info = Info.objects.get(emp = i)
        print(info)
        context['info'] = info
        license = info.license
        print(license)
        qual=license.split(' ')
        context['qual']=qual
        print(qual)

    except Exception as e:
        print(e,'poipoi')

        context['msg'] = msg

    try:
        soldier = Soldier.objects.get(emp = i)
        context['soldier'] = soldier

    except Exception as e:

        context['msg'] = msg


    return render(request, 'result.html', context)

def ocr(request,i):
    print(i,'iiiii')
    paths=[]
    context = {}
    context['menutitle'] = 'OCR READ'
    
    context['imgname']=[]
    resulttext = ''
    context['idx']=i
    
    if 'uploadfile' in request.FILES:
        print(100)
        uploadfile = request.FILES.getlist('uploadfile', '')
        print(uploadfile)
        if uploadfile != '':
            for u in uploadfile:

                name_old = u.name
                
                fs = FileSystemStorage(location = 'static/source')
                imgname= fs.save(f'src-{name_old}', u)
                print(imgname)
                context['imgname'].append(imgname)
                imgfile = Image.open(f'./static/source/{imgname}') 
                path=f'./static/source/{imgname}'
                print(path)
                paths.append(path)
                
<<<<<<< Updated upstream
        #facedetect(paths[0],context['idx'])
        result=naverclova(paths[1],paths[0],context['imgname'][0],context['imgname'][1])
=======
        facedetect(paths[0],context['idx'])
        result=naverclova(paths[1],paths[0],imgname)
>>>>>>> Stashed changes
        context['resulttext1']=result[0]
        context['resulttext2']=[]
        a=result[1:]
        
        for i in enumerate(a):
            
            context['resulttext2'].append(i)

        print(context['resulttext2'])
        context['first']=context['imgname'][0]
        context['remain']=context['imgname']
        context['len']=len(a)
        print(context['len'])

    return render(request,'ocr.html',context)





# -------------------------------------------------------------------------------

# 병역문서 불러오는 부분

def ocrarmy(request,i):
    context = {}
    # print('jfj')
    # print(i)
    # print('ocrarmy')
    if 'uploadfile' in request.FILES:
        
        
        # uploadfile은 html에서 불러오는 것
        uploadfile = request.FILES.get('uploadfile', '')
        print(uploadfile)
        # print('asdfljasdflkj')
            
        if uploadfile != '':
            
            name_old = uploadfile.name



            # 한번에 하려면 여기서 저장하기 전에 네모를 표시해야 한다.


            #fs = FileSystemStorage(location = 'static\source\document_army')    # 이미지들이 저장되는 곳
            fs = FileSystemStorage(location = 'static/source/document_army')    # 이미지들이 저장되는 곳
            imgname= fs.save(f'src-{name_old}', uploadfile)       # 이미지를 저정하는 동작 (이미지명, 이미지파일)
            print(imgname)                                        # 이미지명 확인


            #path=f'static\source\document_army'                   # 이미지를 불러올 경로
            # path=f'static/source/document_army'                   # 이미지를 불러올 경로
            path1=f'static/source/document_army/{imgname}'                   # 이미지를 불러올 경로
            # print(path)


            # ------------------------------------------------- 
            # 만들어둔 EasyOCR을 부르는 부분
            # subhap\ocrtools\armyOCR\easy 경로에서 army.py 에서 call_army를 호출 경로를 보내줌

            # resulttext = call_army(path)    
            # resulttext = call_army(path, imgname)
            # a_info = call_army(path)
            a_in = call_army(path1)
            a_info = a_in[0]
            print(a_info)
            a_text = "군별 : "+a_info['군별']+"\n"+"계급 : "+a_info['계급']+"\n"+"군번 : "+a_info['군번']+"\n"+"역중 : "+a_info['역중']+"\n"+"병과 : "+a_info['병과']+"\n"+"입영일 : "+a_info['입영일']+"\n"+"전역일 : "+a_info['전역일']+"\n"+"전역사유 : "+a_info['전역']


        # --------------------------------------------------------------------


            
            # for a_where in a_in[1]:    # bbox 튜플
            # # for (bbox, text) in results:
            

                

            iii = cv2.imread(os.path.join(path1))

            
            
            for num in ['a','b','c','d','e','f','g','h']:
                (tl, tr, br, bl) = a_in[1][num]
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))

                # 추출한 영역에 사각형
                cv2.rectangle(iii, tl, br, (0, 0, 255), 2)

            img = Image.fromarray(iii)

            img.save(path1)
        





            # ---------------------------------------------------

        context['imgname'] = imgname
        # context['resulttext'] = resulttext
        context['resulttext'] = a_text
        context['a_info1'] = a_info['군별']
        context['a_info2'] = a_info['계급']
        context['a_info3'] = a_info['군번']
        context['a_info4'] = a_info['역중']
        context['a_info5'] = a_info['병과']
        context['a_info6'] = a_info['입영일']
        context['a_info7'] = a_info['전역일']
        context['a_info8'] = a_info['전역']

    context['idx'] = i



    return render(request,'ocrarmy.html',context)



def insertArmy(request, i):

    dbsaved = False

    # 이건 name으로 받아야 함
    a_info1 = request.POST.get("a_info1")
    a_info2 = request.POST.get("a_info2")
    a_info3 = request.POST.get("a_info3")
    a_info4 = request.POST.get("a_info4")
    a_info5 = request.POST.get("a_info5")
    a_info6 = request.POST.get("a_info6")
    a_info7 = request.POST.get("a_info7")
    a_info8 = request.POST.get("a_info8")

    print(a_info1)
    

    kind = a_info1
    s_rank = a_info2
    number = a_info3
    state = a_info4
    depart = a_info5
    on_date = a_info6
    out_date = a_info7
    discharge = a_info8


    try:
        # emp_id를 model.py에서 사용된 emp 로 하면 안된다.
        Soldier.objects.create(emp_id = i, kind = kind, s_rank = s_rank, number = number, state = state, depart = depart, on_date = on_date, out_date = out_date, discharge = discharge)
        # Soldier.objects.create(emp = i, kind = kind, s_rank = s_rank, number = number, state = state, depart = depart, on_date = on_date, out_date = out_date, discharge = discharge)
    except Exception as e:
        print(e)


    context = {
        'idx' : i
    }


    return redirect(f'/info/{i}', context)





def ocrbody(request, i):
    context = {}
    context['idx'] = i
    context['imgname'] = []
    if 'uploadfile' in request.FILES:
        
        uploadfile = request.FILES.getlist('uploadfile', '')
            
        if uploadfile != '':
            for i in uploadfile:
                name_old = i.name
            
                fs = FileSystemStorage(location = 'static/source')
                imgname= fs.save(f'src-{name_old}', i)
                print(imgname)
                context['imgname'].append(imgname)
                imgfile = Image.open(f'./static/source/{imgname}')
                path=f'./static/source/{imgname}'

                resulttext = title_read(imgfile,imgname)
            #지금은 파이테서렉트 쓴것이 리절트 텍스트 
            #은수님의 모듈 결과를 resulttext에 대입해주세요
        
        
                context['resulttext'] = resulttext
        context['first']=context['imgname'][0]
        context['remain']=context['imgname'][0:]


        context['first']=context['imgname'][0]
        context['remain']=context['imgname'][0:]
    return render(request,'ocrbody.html',context)



# 신체정보 insert 함수
def insertBody(request, i):
    # 필요한 data = 사원ID, 키, 몸무게, 시력_(좌, 우), 지병

    height = request.POST.get('height')
    weight = request.POST.get('weight')
    eye_l = request.POST.get('eye_l')
    eye_r = request.POST.get('eye_r')
    disease = request.POST.get('disease')

    try:
        Body.objects.create(emp_id=i, height=height, weight=weight, eye_l=eye_l, eye_r=eye_r, disease=disease)
        print('body table에 insert')
    except Exception as e:
        print(e)

    context = {
        'idx' : i
    }

    return redirect(f'/info/{i}', context)

def ocrresident(request,i):

    savedName = Employees.objects.filter(id=i).values('name')[0]['name']
    
    print("여기일세:", savedName)

    context = {}
    context['idx'] = i
    context['savedName'] = savedName
    

    
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
            #혜지님의 모듈 결과를 resulttext에 대입해주세요


        resulttext=resident(path,imgname) 
        # rrr = cv2.imread(os.path.join(path))
        rrr = cv2.imread(os.path.join(path))
        d1 = resulttext['d1']
        d2 = resulttext['d2']
        cv2.rectangle(rrr, pt1=(d1[0], d1[2]), pt2=(d1[1], d1[3]), color=(0,0,255), thickness=2)
        cv2.rectangle(rrr, pt1=(d2[0], d2[2]), pt2=(d2[1], d2[3]), color=(0,0,255), thickness=2)
        sss = Image.fromarray(rrr)
        sss.save(f'./static/imgr/{imgname}')

        context['imgname'] = imgname
        context['resulttext'] = resulttext


    return render(request,'ocrresident.html',context)

def insertResident(request, i):

    resi_num = request.POST.get("r_resi_num")
    addr = request.POST.get("r_addr")

    print("잘받아오나?", i, resi_num, addr)

    try:
        Employees.objects.filter(id=i).update(resi_num=resi_num, addr=addr)
    except Exception as e:
        print(e)

    context = {
        'idx' : i
    }

    return redirect(f'/info/{i}', context)


from datetime import datetime
def stats(request):
    # employees.gender(성비)
    # employees.birth(연령대)
    # info.salary(연봉) (x:사원수, y:연봉)
    # employees.hire_date입사율
    # employees.class 퇴사율
    # t년도의 퇴사율=t년도 퇴사자수/t-1년도 말의 재직자 수
    
    employees = Employees.objects.all()
    
    ##### 성비
    women = Employees.objects.filter(gender=1)
    men = Employees.objects.filter(gender=0)
    per_women = len(women) / len(employees) * 100
    per_men = len(men) / len(employees) * 100



    ##### 연령대
    birth = Employees.objects.filter().values('birth')
    print("응애", datetime.today().year, type(datetime.today().year))

    def get_age(birth):
        born = "19" + birth[:2]
        age = datetime.today().year - int(born) + 1
        return age

    age_20s = 0
    age_30s = 0
    age_40s = 0
    age_50s = 0
    age_60s = 0
    age_else = 0

    # employees들의 나이를 연령대별로 나누고 수를 도출
    for i in birth:
        # print(i['birth'], type(i['birth']))
        age = get_age(i['birth'])  # int타입의 나이가 도출
        div = int(age/10)
        if div == 2:
            age_20s += 1
        elif div == 3:
            age_30s += 1
        elif div == 4:
            age_40s += 1
        elif div == 5:
            age_50s += 1
        elif div == 6:
            age_60s += 1
        else:
            age_else += 1
            
    print(age_20s, age_30s, age_40s, age_50s, age_60s, age_else)



    ##### 입사율 
    hire = Employees.objects.filter().values('hire_date')

    # 입사율 구하는 함수 ((t년도의 입사율=t년도 채용자수/t-1년도 말의 재직자 수))
    def hire_rate(year):
        hire_cnt = 0
        worker_cnt = 0

        for i in hire:
            hire_year = i['hire_date'][:4]
        
            if hire_year < str(year):
                worker_cnt += 1
            elif hire_year == str(year):
                hire_cnt += 1

        # print(year, "년도에 대한 입사율 : ", hire_cnt / worker_cnt * 100)
        return hire_cnt / worker_cnt * 100

    # print("입사율 : ",hire_rate(2020), hire_rate(2019), hire_rate(2018), hire_rate(2017), hire_rate(2016))

    hire_rate_dic = {}
    for i in range(6):
        year = datetime.today().year - (i+1)
        hire_rate_dic.setdefault(str(year), hire_rate(year))
        
    print("입사율 dic : ", hire_rate_dic)

    # js for문 귀찮으니 미리 뺴놓자   
    hr_2021 = hire_rate_dic['2021']
    hr_2020 = hire_rate_dic['2020']
    hr_2019 = hire_rate_dic['2019']
    hr_2018 = hire_rate_dic['2018']
    hr_2017 = hire_rate_dic['2017']
    hr_2016 = hire_rate_dic['2016']



    ##### 퇴사율
    resign = Employees.objects.filter(class_field="퇴사")

    # 퇴사율 구하는 함수 (t년도의 퇴사율=t년도 퇴사자수/t-1년도 말의 재직자 수)
    # def resign_rate():




    context = {
        "employees": employees,
        "per_women": per_women,
        "per_men": per_men,
        "age_20s": age_20s,
        "age_30s": age_30s,
        "age_40s": age_40s,
        "age_50s": age_50s,
        "age_60s": age_60s,
        "age_else": age_else,
        # "hire_rate": hire_rate,  # 딕셔너리
        "hr_2021": hr_2021,
        "hr_2020": hr_2020,
        "hr_2019": hr_2019,
        "hr_2018": hr_2018,
        "hr_2017": hr_2017,
        "hr_2016": hr_2016,

    }

    return render(request, 'stats.html', context)


def insertResume(request,i):
    # 필요한 data = 사원ID, 키, 몸무게, 시력_(좌, 우), 지병

    length = int(request.POST.get('len'))
    print(length)
    qual=''
    gr=request.POST.get('gradu')
    for l in range(length):
        ja=request.POST.get('{}'.format(l))
        print(ja)
        qual+=ja.strip()
        qual+=' '
        print(qual) 

    try:
        Info.objects.create(emp_id=i,graduation=gr,license=qual)
        print('info table에 insert')
    except Exception as e:
        print(e)

    context = {
        'idx' : i
    }

    return redirect(f'/info/{i}', context)


def ocrcont(request,i):
    context = {}
    context['idx'] = i
    if 'uploadfile' in request.FILES:
        
        uploadfile = request.FILES.get('uploadfile', '')
            
        if uploadfile != '':
            name_old = uploadfile.name
            
            fs = FileSystemStorage(location = 'static/source')
            imgname= fs.save(f'src-{name_old}', uploadfile)
            print(imgname)
            print(type(uploadfile))
            imgfile = Image.open(f'./static/source/{imgname}')
            path=f'./static/source/{imgname}'
            
        resulttext=task(path,imgname) 
        context['imgname'] = imgname
        context['resulttext'] = resulttext


    return render(request,'ocrcont.html',context)

def insertCont(request,i):
    task = request.POST.get("task")
    sal = request.POST.get("salary")
    #addr = request.POST.get("r_addr")

    print("잘받아오나?", i, task)

    try:
        Info.objects.filter(emp_id=i).update(task=task, salary=sal)
    except Exception as e:
        print(e)

    context = {
        'idx' : i
    }

    return redirect(f'/info/{i}', context)
