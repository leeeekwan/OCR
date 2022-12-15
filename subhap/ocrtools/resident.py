import os
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
import easyocr
plt.style.use('seaborn-white')
# from PIL import ImageFont, ImageDraw, Image
import re


def resident(img):
    img=np.array(img)



    # base_path = r'C:\DevRoot\Dropbox\Py04\10_ComputerVision\add'
    # img = cv2.imread(os.path.join(base_path, 'resident2.png'))


    img_re = cv2.resize(img, (0,0), fx=2, fy=2)

    tot_y, tot_x, _ = img_re.shape
    gray = cv2.cvtColor(img_re, cv2.COLOR_BGR2GRAY)
    _, blue_th = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)

    temp = np.zeros(img_re.shape, dtype=np.uint8)
    con_area={}

    # 외곽선 검출
    contours, _ = cv2.findContours(
        blue_th,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_NONE,
    )

    for pts in contours:
        x, y, w, h = cv2.boundingRect(pts)
        
        approx = cv2.approxPolyDP(
                pts,
                cv2.arcLength(pts, True) * 0.02,
                True,
        )
        if len(approx) != 4: continue
        if (cv2.contourArea(pts) > 1000000) or (cv2.contourArea(pts) < 800000): continue
        
        # dic = {xywh : Area} 저장
        con_area.setdefault((x, y, w, h), cv2.contourArea(pts))
        cv2.polylines(temp, pts, True, (135, 135, 0), 7)
        
    # 발급일자
    # 1) contour들 중 최소 y좌표를 가진 box
    temp_y = tot_y  # img의 최대 y좌표
    for i in con_area.keys():    # con_area의 y좌표 최솟값 구하기
        if i[1] < temp_y:
            temp_y = i[1]
            temp_x = i[0]
            temp_w = i[2]
            temp_h = i[3]


    # easyocr
    reader = easyocr.Reader(['ko', 'en'], gpu=False)
    result = reader.readtext(img_re)


    check_addr = False
    check_rel = False 
    check_my = False
    check_lov = False
    check_child = False

    # 각 조건에 맞는 xy 좌표(비율) 찾기
    while True:
        for tu in result:
            read_x = tu[0][0][0]
            read_y = tu[0][0][1]
            read_w = tu[0][1][0] - tu[0][0][0]
            read_h = tu[0][2][1] - tu[0][1][1]
            
            # first box(레이블행)
            if (tot_x * 0.06 < read_x < tot_x * 0.14) and (tot_y * 0.23 < read_y < tot_y * 0.41):

                if tu[1] == "현주소:":
                    # 현주소의 xy좌표값 변수에 저장
                    tag_x1 = tu[0][0][0]
                    tag_x2 = tu[0][1][0]
                    tag_y1 = tu[0][0][1]
                    tag_y2 = tu[0][2][1]

                    # 현주소값에 대한 box matching
                    addr_x1 = tag_x2
                    addr_x2 = tag_x2 + int(tot_x * 0.5)
                    addr_y1 = tag_y1 - int(tot_y * 0.013)
                    addr_y2 = tag_y2 + int(tot_y * 0.013)
                    check_addr = True
                    
                elif tu[1] == "번호":
                    # 번호 태그의 xy 좌표값 저장
                    no_x1 = tu[0][0][0]
                    no_x2 = tu[0][1][0]
                    no_y1 = tu[0][0][1]
                    no_y2 = tu[0][2][1] 

                    # 세대주 관계에 대한 box matching
                    rel_x1 = no_x2 + int(tot_x * 0.015)
                    rel_x2 = no_x2 + int(tot_x * 0.1)
                    rel_y1 = no_y1 + int(tot_y * 0.023)
                    rel_y2 = no_y2 + int(tot_y * 0.35)
                    check_rel = True

        if check_addr and check_rel:
            for tu in result:
                read_x = tu[0][0][0]
                read_y = tu[0][0][1]
                read_w = tu[0][1][0] - tu[0][0][0]
                read_h = tu[0][2][1] - tu[0][1][1]
                
                # secondary box(세대주 관계)
                if (rel_x1 < read_x < rel_x2) and (rel_y1 < read_y < rel_y2):
                    
                    if tu[1] == "본인":
                        # 본인 태그에 대한 xy 좌표
                        me_x = (tu[0][0][0] + tu[0][1][0]) / 2  # 두 x좌표의 평균값
                        me_y1 = tu[0][0][1]
                        me_y2 = tu[0][2][1]

                        # '나'의 이름 / 주민등록번호 xy 좌표
                        myname_x1 = me_x + int(tot_x * 0.03)
                        myname_x2 = me_x + int(tot_x * 0.18)
                        myname_y1 = me_y1 - int(tot_y * 0.01)
                        myname_y2 = me_y2 + int(tot_y * 0.01)
                        check_my = True

                    if tu[1] == "배우자":
                        # 배우자 태그에 대한 xy 좌표
                        lover_x = (tu[0][0][0] + tu[0][1][0]) / 2
                        lover_y1 = tu[0][0][1]
                        lover_y2 = tu[0][2][1]

                        # 배우자의 이름 / 주민등록번호 xy 좌표
                        l_name_x1 = lover_x + int(tot_x * 0.03)
                        l_name_x2 = lover_x + int(tot_x * 0.18)
                        l_name_y1 = lover_y1 - int(tot_y * 0.01)
                        l_name_y2 = lover_y2 + int(tot_y * 0.01)
                        check_lov = True


                    if tu[1] == "자녀" or "자":
                        # 자녀 태그에 대한 xy 좌표
                        child_x = (tu[0][0][0] + tu[0][1][0]) / 2
                        child_y1 = tu[0][0][1]
                        child_y2 = tu[0][2][1]

                        # 자녀의 이름 / 주민등록번호 xy 좌표
                        c_name_x1 = child_x + int(tot_x * 0.03)
                        c_name_x2 = child_x + int(tot_x * 0.18)
                        c_name_y1 = child_y1 - int(tot_y * 0.01)
                        c_name_y2 = child_y2 + int(tot_y * 0.01)
                        check_child = True
                        
                    # if tu[1] == "형" or "제" or "누이" or "매" or "누나" or "오빠":
                        
            
            if check_addr and check_rel and check_my:
                break

    # OCR 출력
    addr_pre2=""
    for tu in result:
        read_x = tu[0][0][0]
        read_y = tu[0][0][1]
        read_w = tu[0][1][0] - tu[0][0][0]
        read_h = tu[0][2][1] - tu[0][1][1]

        
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
            
        
        # 배우자 이름
        if check_lov == True and\
        l_name_x1 < read_x < l_name_x2 and l_name_y1 < read_y < l_name_y2:
            pre = tu[1].strip()
            if re.match('\D', pre[0]):
                lover_name = pre
            
            
        # 자녀 이름
        if check_child == True and\
        c_name_x1 < read_x < c_name_x2 and c_name_y1 < read_y < c_name_y2:
            pre = tu[1].strip()
            if re.match('\D', pre[0]):
                child_name = pre
                
        if temp_x < read_x < temp_x + temp_w and temp_y + temp_h < read_y < temp_y + 1.2 * temp_h:
            cv2.rectangle(
                img_re,
                pt1=(temp_x, temp_y + temp_h),
                pt2=(temp_x + temp_w, temp_y + int(1.2 * temp_h)),
                color=(230, 255, 12),
                thickness=15,
            )
            pre = tu[1]
            issue_date = pre
            

            
            
    print("이름 : ", name)
    print("주민번호 : ", resi_num)
            
    addr = addr_pre2.strip()
    print("현주소 : ", addr)

    # if check_lov == True:
    #     print("배우자 : ", lover_name)
        
    # if check_child == True:
    #     print("자녀 : ", child_name)
    print("발급일자 : ", issue_date)


    resi_dic = {}
    resi_dic['name'] = name
    resi_dic['resi_num'] = resi_num
    resi_dic['addr'] = addr
    resi_dic['issue_date'] = issue_date



    return resi_dic




















