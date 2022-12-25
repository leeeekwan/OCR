import os
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
import easyocr
import pandas as pd
plt.style.use('seaborn-white')
# from PIL import ImageFont, ImageDraw, Image
import re

def reorderPts(pts):
    idx = np.lexsort((pts[:, 1], pts[:, 0]))  # 칼럼0 -> 칼럼1 순으로 정렬한 인덱스를 반환
    pts = pts[idx]  # x좌표로 정렬

    if pts[0, 1] > pts[1, 1]:
        pts[[0, 1]] = pts[[1, 0]]

    if pts[2, 1] < pts[3, 1]:
        pts[[2, 3]] = pts[[3, 2]]

    return pts

# (커스텀)임계값 찾는 함수
def searchth(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_small = cv2.resize(gray, dsize=None, fx=0.1, fy=0.1, interpolation=cv2.INTER_AREA)
    sm = pd.Series(gray_small.ravel())
    new_sm = sm.value_counts().sort_index()                 #(x: 값, y: 개수) # 인덱스 오름차순 정렬
    idx = list(new_sm.index)

    cnt=0
    dic={}
    x_li = {}
    for i in idx:
        cnt+=1
        if new_sm[i] > temp:
            temp = new_sm[i]
        if cnt % 10 ==0:
            dic[cnt]=temp
            temp=0

    for i in list(dic.keys()):
        if i != list(dic.keys())[-1] and i != list(dic.keys())[-2]:
            if dic[i] < dic[i+10] and dic[i+10] > dic[i+20] and i!=120:
                print("근사화 그래프의 극댓점의 x값", i+10)
                x_li.append(i+10)

    # 극댓점의 x값의 평균값을 커스텀 임계값으로 설정
    x_li.remove(max(x_li)) # 이때 x_li의 최댓값(흰바탕) 을 제외
    th = int(sum(x_li) / len(x_li))
    return th



def resident(path):
    img=cv2.imread(os.path.join(path))

    img_re = cv2.resize(img, (0,0), fx=2, fy=2)

    gray = cv2.cvtColor(img_re, cv2.COLOR_BGR2GRAY)
    _, img_th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # 출력 영상 설정
    dw, dh = 4958, 7016
    srcQuad = np.array([[0, 0], [0, 0], [0, 0], [0, 0]], np.float32)
    dstQuad = np.array([[0, 0], [0, dh], [dw, dh], [dw, 0]], np.float32)
    dst = np.zeros((dh, dw), np.uint8) 

    contours, _ = cv2.findContours(
    img_th,
    cv2.RETR_LIST,
    cv2.CHAIN_APPROX_NONE,
    )

    # 용지 4점 잡기
    for pts in contours:
        
        if cv2.contourArea(pts) < 40000000: continue
        
        approx = cv2.approxPolyDP(
            pts,
            cv2.arcLength(pts, True) * 0.02,
            True,
        )
        
        if len(approx) != 4: continue
        
        cv2.polylines(img_re, [approx], True, (0, 255, 0), 2, cv2.LINE_AA)
        srcQuad = reorderPts(approx.reshape(4, 2).astype(np.float32))  # 정렬된 결과를 srcQuad에 저장
        
        pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
        dst = cv2.warpPerspective(img_re, pers, (dw, dh), 
                                flags=cv2.INTER_CUBIC
                                )
    # OCR 가능한 전처리된 img
    pre_img = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)


    # 처리된 img 좌표잡기 + OCR
    tot_y, tot_x, _ = pre_img.shape
    reader = easyocr.Reader(['ko', 'en'], gpu=False)
    result = reader.readtext(pre_img)

    # print(result)

    # 각 조건에 맞는 xy 좌표(비율) 찾기
    for tu in result:
        read_x = tu[0][0][0]
        read_y = tu[0][0][1]

        if tu[1] == "현주소:":
            # 현주소의 xy좌표값 변수에 저장
            # tag_x1 = tu[0][0][0]
            tag_x2 = tu[0][1][0]
            tag_y1 = tu[0][0][1]
            tag_y2 = tu[0][2][1]

            # 현주소값에 대한 box matching
            addr_x1 = tag_x2
            addr_x2 = tag_x2 + int(tot_x * 0.5)
            addr_y1 = tag_y1 - int(tot_y * 0.013)
            addr_y2 = tag_y2 + int(tot_y * 0.013)
            print(addr_x1, addr_x2, addr_y1, addr_y2)

        # elif tu[1] == "번호":
        #     # 번호 태그의 xy 좌표값 저장
        #     # no_x1 = tu[0][0][0]
        #     no_x2 = tu[0][1][0]
        #     no_y1 = tu[0][0][1]
        #     no_y2 = tu[0][2][1] 

            # 세대주 관계에 대한 box matching
            # rel_x1 = no_x2 + int(tot_x * 0.015)
            # rel_x2 = no_x2 + int(tot_x * 0.1)
            # rel_y1 = no_y1 + int(tot_y * 0.023)
            # rel_y2 = no_y2 + int(tot_y * 0.35)
            
        elif tu[1] == "본인":
            # 본인 태그에 대한 xy 좌표
            me_x = (tu[0][0][0] + tu[0][1][0]) / 2  # 두 x좌표의 평균값
            me_y1 = tu[0][0][1]
            me_y2 = tu[0][2][1]

            # '나'의 이름 / 주민등록번호 xy 좌표
            myname_x1 = int(me_x + int(tot_x * 0.03))
            myname_x2 = int(me_x + int(tot_x * 0.18))
            myname_y1 = me_y1 - int(tot_y * 0.01)
            myname_y2 = me_y2 + int(tot_y * 0.007)

                
    # OCR 출력
    addr_pre2=""
    for tu in result:
        read_x = tu[0][0][0]
        read_y = tu[0][0][1]

        
        # 현주소 출력
        if addr_x1 < read_x < addr_x2 and addr_y1 < read_y < addr_y2:
            addr_pre1 = " ".join(tu[1].split())
            addr_pre2 += " " + addr_pre1
            
            
        # 본인의 이름 + 주민등록번호 출력
        if myname_x1 < read_x < myname_x2 and myname_y1 < read_y < myname_y2:
            pre = tu[1].strip()
            if re.match('\D', pre[0]): # 이름 일 때
                name = pre
            elif re.match('[0-9]', pre[0]): # 주민번호 일 때
                resi_num = pre


    # print("이름 : ", name)
    # print("주민번호 : ", resi_num)
            
    addr = addr_pre2.strip()
    # print("현주소 : ", addr)



    resi_dic = {}
    resi_dic['name'] = name
    resi_dic['resi_num'] = resi_num
    resi_dic['addr'] = addr
    # resi_dic['d1'] = (addr_x1, addr_x2, addr_y1, addr_y2)
    # resi_dic['d2'] = (myname_x1, myname_x2, myname_y1, myname_y2)




    return resi_dic




















