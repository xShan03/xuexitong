# 滑动验证码处理模块
import cv2
import numpy as np


# 对滑块做精细化处理
def fix_img(filename):
    img = cv2.imdecode(np.array(bytearray(filename), dtype='uint8'), cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour_img = cv2.drawContours(img, contours, 0, (0, 255, 0), 1)
    x, y, w, h = cv2.boundingRect(contours[0])
    mixintu = contour_img[y:y + h, x:x + w]
    return mixintu


# 主方法
def main(fadebg, fullbg):
    """
    处理滑块验证码
    @param fadebg: 滑块图
    @param fullbg: 背景图
    @return: 'cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED'的对比结果以及最佳位移值
    """
    tp_img = fix_img(fadebg)
    tp_edge = cv2.Canny(tp_img, 100, 200)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2BGR)
    bg_img = cv2.imdecode(np.array(bytearray(fullbg), dtype='uint8'), cv2.IMREAD_UNCHANGED)
    bg_edge = cv2.Canny(bg_img, 100, 200)
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2BGR)
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED']
    results = {}
    move = 0
    for meth in methods:
        temp_full_img = bg_pic.copy()
        res = cv2.matchTemplate(temp_full_img, tp_pic, eval(meth))
        loc = cv2.minMaxLoc(res)[3]
        results[meth] = loc
        move = loc[0]
    return results, move
