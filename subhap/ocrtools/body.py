import os
import sys
import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageFont, Image, ImageDraw
plt.style.use('seaborn-white')


# def three_img(img1, img2, img3):
#     cvtImg1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
#     cvtImg2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
#     cvtImg3 = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)
    
#     plt.figure(figsize=(15, 7))
#     plt.subplot(131), plt.imshow(cvtImg1)
#     plt.subplot(132), plt.imshow(cvtImg2)
#     plt.subplot(133), plt.imshow(cvtImg3)
#     plt.show()



# def plt_imshow_bgr(bgr_img):
#     cvtImg = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
#     plt.imshow(cvtImg)
#     plt.show()


def reorderPts(pts):
    idx = np.lexsort((pts[:, 1], pts[:, 0]))  # 칼럼0 -> 칼럼1 순으로 정렬한 인덱스를 반환
    pts = pts[idx]  # x좌표로 정렬

    if pts[0, 1] > pts[1, 1]:
        pts[[0, 1]] = pts[[1, 0]]

    if pts[2, 1] < pts[3, 1]:
        pts[[2, 3]] = pts[[3, 2]]

    return pts


def img_process(img):
    img = np.array(img)
    rr = img.copy()
    rr = cv2.resize(rr, (0, 0), fx = 2, fy = 2)


    copy1 = img.copy()
    copy1 = copy1[:, :, 2]
    # copy1 = cv2.cvtColor(copy1, cv2.COLOR_BGR2GRAY)
    re_body1 = cv2.resize(copy1, (0, 0), fx = 2, fy = 2)
    src_temp = re_body1.copy()

    _, src_bin1 = cv2.threshold(src_temp, 
                                0, 
                                255, 
                                cv2.THRESH_BINARY | cv2.THRESH_OTSU
                            )

    # 출력 영상 설정
    dw, dh = 1000, 1400
    srcQuad = np.array([[0, 0], [0, 0], [0, 0], [0, 0]], np.float32)
    dstQuad = np.array([[0, 0], [0, dh], [dw, dh], [dw, 0]], np.float32)
    #dst = np.zeros((dh, dw), np.uint8)

    # 외각선 검출
    contours, _ = cv2.findContours(
        src_bin1, 
        cv2.RETR_EXTERNAL,   # mode
        cv2.CHAIN_APPROX_NONE,   # method
    )

    for pts in contours:
        
        # 면적이 1000보다 작으면 빼기
        if cv2.contourArea(pts) < 800000: continue
            
        # 근사화 함수
        approx = cv2.approxPolyDP(
            pts,
            cv2.arcLength(pts, True) * 0.02,
            True,   # closed
        )
        
        print(approx)
        
        if not cv2.isContourConvex(approx) or len(approx) != 4:
            continue
            
        cv2.polylines(rr, [approx], True, (0, 255, 0), 2, cv2.LINE_AA)
        srcQuad = reorderPts(approx.reshape(4, 2).astype(np.float32))  # !!
            
        pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
        dst = cv2.warpPerspective(rr, pers, (dw, dh), 
                                flags=cv2.INTER_CUBIC
                                )

        
    return dst

# 박스봐표 가공 함수
def make_pt(what_x, what_y, first, last):
    pt1 = (
        what_x[0] + first[0],
        what_y[0] + first[1]
          )
    pt2 = (
        what_x[0] + last[0],
        what_y[0] + last[1]
        )
    
    pt = (pt1, pt2)
    
    return pt

# 데이터 저장소
xy_data = {
    'titleX' : (100, 1900),
    'titleY' : (250, 430),
    'firstX' : (700, 1500),
    'firstY' : (2350, 2480),
    'secondX' : (340, 1800),
    'secondY' : (330, 800),
    'thirdX' : (200, 1650),
    'thirdY' : (1480, 1850)
          }

img_data = {}

resulttext = {'date' : ''}   # date, disease, height, weight, eye_L, eye_R


# OCR
def title_read(img, name):

    img = np.array(img)

    dst = img_process(img)
    dst = cv2.resize(dst, (0,0), fx=2, fy=2)

    
    reader = easyocr.Reader(['ko'], gpu=False)
    title = reader.readtext(dst[xy_data['titleY'][0]:xy_data['titleY'][1], xy_data['titleX'][0]:xy_data['titleX'][1]])
    
    print(title)

    for ti in title:
        if "심뇌" in ti[1]:   # 날짜
            print(f'{ti[1]} body1')

            # 좌표
            pt = make_pt(xy_data['titleX'], xy_data['titleY'], ti[0][0], ti[0][2])
            
            # 제목부분 박스
            dst = cv2.rectangle(dst, pt[0], pt[1], (255, 0, 0), thickness = 3)
               
            result = reader.readtext(dst[
                xy_data['firstY'][0]:xy_data['firstY'][1],
                xy_data['firstX'][0]:xy_data['firstX'][1]
            ])
            
            for dt in result:
                resulttext['date'] += dt[1]

                # 좌표
                pt = make_pt(xy_data['firstX'], xy_data['firstY'], dt[0][0], dt[0][2])
            
                # 날짜부분 박스
                dst = cv2.rectangle(dst, pt[0], pt[1], (255, 0, 0), thickness = 3)

                img=Image.fromarray(dst)
                img.save(f'./static/imgr/{name}')
                
                # img_data['img1'] = dst

            print(resulttext['date'])
                        
                
            break
        
        elif "건강검진" in ti[1]:   # 유질환
            print(f'{ti[1]} body3')

            # 좌표
            pt = make_pt(xy_data['titleX'], xy_data['titleY'], ti[0][0], ti[0][2])

            # 제목부분 박스
            dst = cv2.rectangle(dst, pt[0], pt[1], (255, 0, 0), thickness = 3)
            
            
            result = reader.readtext(dst[
                xy_data['thirdY'][0]:xy_data['thirdY'][1],
                xy_data['thirdX'][0]:xy_data['thirdX'][1]
            ])
            
            
            for i in range(len(result)):
                if result[i][1] == "유질환" or result[i][1] == "유절판" or result[i][1] == '유절환':
                    resulttext['disease'] = result[i + 1][1]

                    # 좌표
                    pt = make_pt(xy_data['thirdX'], xy_data['thirdY'], result[i][0][0], result[i][0][2])

                    # 유질환 제목부분 박스
                    dst = cv2.rectangle(dst, pt[0], pt[1], (255, 0, 0), thickness = 3)
                    
                    #-----------------------------------------------------------

                    # 좌표
                    pt = make_pt(xy_data['thirdX'], xy_data['thirdY'], result[i + 1][0][0], result[i + 1][0][2])

                    # 유질환부분 박스
                    dst = cv2.rectangle(dst, pt[0], pt[1], (255, 0, 0), thickness = 3)
                    
                    
            print(resulttext['disease'])

            img=Image.fromarray(dst)
            img.save(f'./static/imgr/{name}')

            # img_data['img2'] = dst
            
            break
        
        else:               # 키, 몸무게, 청력, 시력
            print(f'{ti[1]} body3')

            print('키, 몸무게 shape = ')
            print(dst.shape)
            
            result = reader.readtext(dst[
                xy_data['secondY'][0]:xy_data['secondY'][1],
                xy_data['secondX'][0]:xy_data['secondX'][1]
            ])

            print(result)
                
            
            for i in range(len(result)):
                if "및 몸무게" in result[i][1] or "무게" in result[i][1]:
                    resulttext['height'] = result[i + 1][1]
                    resulttext['weight'] = result[i + 2][1]

                    # 좌표
                    pt = make_pt(xy_data['secondX'], xy_data['secondY'], result[i][0][0], result[i][0][2])

                    # 키, 몸무게 제목부분 박스
                    dst = cv2.rectangle(dst, pt[0], pt[1], (255, 0, 0), thickness = 3)
                    
                    
                    # 좌표
                    pt = make_pt(xy_data['secondX'], xy_data['secondY'], result[i + 1][0][0], result[i + 1][0][2])

                    # 키 부분 박스
                    dst = cv2.rectangle(dst, pt[0], pt[1], (255, 0, 0), thickness = 3)
                    
                    
                    # 좌표
                    pt = make_pt(xy_data['secondX'], xy_data['secondY'], result[i + 2][0][0], result[i + 2][0][2])

                    # 몸무게 제목부분 박스
                    dst = cv2.rectangle(dst, pt[0], pt[1], (255, 0, 0), thickness = 3)

                
                    print(resulttext['height'], resulttext['weight'])
                
                if '시력' in result[i][1] or '시디' in result[i][1]:
                    resulttext['eye_l'] = result[i + 1][1]
                    resulttext['eye_r'] = result[i + 3][1]

                    # 좌표
                    pt = make_pt(xy_data['secondX'], xy_data['secondY'], result[i][0][0], result[i][0][2])

                    # 시력 제목부분 박스
                    dst = cv2.rectangle(dst, pt[0], pt[1], (255, 0, 0), thickness = 3)
                    
                    
                    # 좌표
                    pt = make_pt(xy_data['secondX'], xy_data['secondY'], result[i + 1][0][0], result[i + 1][0][2])

                    # 왼쪽 부분 박스
                    dst = cv2.rectangle(dst, pt[0], pt[1], (255, 0, 0), thickness = 3)
                    
                    
                    # 좌표
                    pt = make_pt(xy_data['secondX'], xy_data['secondY'], result[i + 3][0][0], result[i + 2][0][2])

                    # 오른쪽 부분 박스
                    dst = cv2.rectangle(dst, pt[0], pt[1], (255, 0, 0), thickness = 3)
                    
                
            print(resulttext['eye_l'], resulttext['eye_r'])

            img=Image.fromarray(dst)
            img.save(f'./static/imgr/{name}')

            # img_data['img3'] = img

            break
        

    return resulttext







