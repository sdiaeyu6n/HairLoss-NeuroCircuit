import cv2
import numpy as np
import requests
# filepath 얻어오는 이 문제 해결하면 바꾸기.
# def caculate_ratio(requestImage):
def caculate_ratio():
    # html에서 image로 불러온걸 어떻게 numpy.array로 바꿔야할지 모르겠다.. 혹은 filepath를 받아오는법..
    # (1)
    # image_nparray = np.asarray(bytearray(requestImage), dtype=np.uint8)
    # image = cv2.imdecode(tmp_length, cv2.IMREAD_COLOR)
    # resize_image = cv2.resize(image, dsize=(221, 300))  # resize

    # (2)
    # image_nparray = np.asarray(bytearray(requests.get(filepath).content), dtype=np.uint8)
    # image = cv2.imdecode(tmp_length, cv2.IMREAD_COLOR)
    # resize_image = cv2.resize(image, dsize=(221, 300))  # resize

    # (3)
    # tmp_length = sum(1 for el in requestImage())
    # tmp_array = numpy.empty(tmp_length)
    # for i, el in enumerate(requestImage()): tmp_array[i] = el
    # resize_image = cv2.resize(tmp_array, dsize=(221, 300))  # resize

    # (4)
    image = cv2.imread('C:/Users/user/bayabas/test_upload_image.jpg', cv2.IMREAD_COLOR)
    resize_image = cv2.resize(image, dsize=(221, 300)) # resize

    ## Guideline Mask
    guideline = cv2.imread("C:/Users/user/0_guideline_mask.jpg", cv2.IMREAD_COLOR) # guideline mask 불러오기
    guideline1 = cv2.resize(guideline, (300, 221)) # resize
    # 2차원으로 만들기 -> hsv 로 하얀색 따오기
    guideline_image_hsv = cv2.cvtColor(guideline1, cv2.COLOR_BGR2HSV) # BGR에서 HSV로 변환
    lower_white = np.array([0,0,200]) # HSV 흰색 하한
    upper_white = np.array([180,255,255]) # HSV 흰색 상한
    guideline_mask = cv2.inRange(guideline_image_hsv, lower_white, upper_white) # mask

    ## Rare Image
    hsvLower = np.array([0, 2, 80]) # 추출할 두피색의 하한(HSV)
    hsvUpper = np.array([51, 100, 255]) # 추출할 두피색의 상한(HSV)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # 이미지를 HSV으로 변환
    hsv_mask = cv2.inRange(hsv, hsvLower, hsvUpper) # HSV에서 마스크를 작성

    ## Image mask "AND" Guideline mask
    mask_result = cv2.bitwise_and(guideline_mask, hsv_mask) # 원래 이미지와 마스크를 합성
    # cv2.imwrite('2_mask_con_img.jpg', mask_result)

    up, down = 0, 0
    for i in range(len(mask_result)):
        for x, y in zip(mask_result[i], guideline_mask[i]):
            if x == 255:
                up +=1
            if y == 255:
                down += 1

    scalp_ratio = up / down * 100

    return scalp_ratio