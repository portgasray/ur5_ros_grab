import cv2
import numpy as np
import os
import time
from enum import Enum
import math
import imutils

### read file name from floder
def read_file_name(root_dir):
    entries = os.listdir(root_dir)
    for entry in entries:
    # for file in os.listdir(os.path.join(os.path.dirname(root_dir)):
        file_name.append(str(entry))
    total_files = len(file_name)
    print (str(total_files) + " images in source directory")
    for items in file_name:
        print (items)
    return file_name


###Loading image
def load_image(file_name):
    image_address = 'images/' + file_name
    print ('Image: ' +image_address+' is processing')
    # image_address = 'src_images/yuan_pi.jpg'
    src_image = cv2.imread(image_address, 1)
    if src_image is None:
        print ("Image failed to load")
    else:
        print ("Image loaded")
    return src_image

### find contours of sharpe
def find_contours_sharpe(src_image):
    # convert image to grayscale image
    gray_image =  cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)

    # 模糊化（降噪）
    kernel_size = 13 # 必须是奇数
    radius = 2
    blurred_image = cv2.GaussianBlur(gray_image , (kernel_size, kernel_size) , radius)
    if blurred_image is not None:
        print ("Image blurred")

    #convert the grayscale image to binary image (二值化)
    threshold = 126
    max_value = 225
    ret, thresh = cv2.threshold(blurred_image, threshold, max_value, cv2.THRESH_BINARY)
    if thresh is not None:
        print ("Threshold complete")

    #Finding contours
    # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_count = len(contours)
    if contours is not None:
        print (str(contours_count) + " contours found in total")
    return contours,hierarchy

### find the main contour (biggest area)
def find_biggest_contour(contours):
    cnt = contours[0]
    max_area = cv2.contourArea[cnt]
    for cont in contours:
        if cv2.contourArea(cont) > max_area:
            cnt = contour
            max_area = cv2.contourArea(cont)
    return cnt

def contours_filter(src_image, contours):
    #过滤轮廓

    print ("The largest contour has area of: " + str(max_contour_area) +
           ", with index of: " + str(max_contour_index))
    contour_qualified_index = max_contour_index
    return contour_qualified_index

### find centroid  coordinate of blob
def find_ceteroid_shape(contour):
    ###centroid of a shape
    # calculate momnets of binary image
    M = cv2.moments(contour)
    # M = cv2.moments(thresh)
    # calculate x, y coordinate of center
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0
    return cX, cY

### define main contour approx. and hull
def draw_fitting_contour(src_image, cnt):
    canvas = np.zeros(src_image.shape, np.uint8)
    perimeter = cv2.arcLength(cnt, True)
    epslion = 0.01 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epslion, True)
    # Convex Hull
    hull = cv2.convexHull(cnt)
    return approx, hull
    # contours_dst = cv2.drawContours(canvas, [approx], -1, (0, 0, 255), 3)
    # return contours_dst

### draw biggest contour and center of the contour
def draw_contour_and_centroid(src_image, contour, cX, cY, rgb = '(255,255,255)', thickness = 3):
    # Make a black canvas image for drawing contours 制作黑色背景图（用于下面轮廓绘制的背景）
    # ret, black_canvas = cv2.threshold(src_image, 255, 0, cv2.THRESH_BINARY)
    # if black_canvas is not None:
    #     print ("Black canvas image made")

    # drawing contour
    contours_dst = cv2.drawContours(src_image, contour, -1, rgb, 2)
    if contours_dst is not None:
        print ("Contours drawn")
    # put text and highlight the center
    cv2.circle(contours_dst, (cX, cY), 1, (255, 255, 255), -1)
    cv2.putText(contours_dst, "center", (cX - 20, cY - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
    return contours_dst

def display_contour_centroid(contours_dst):
    cv2.namedWindow('src_image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('src_image', 1080, 800)
    cv2.imshow('src_image', contours_dst)
    # cv2.waitKey(200)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # if k == 27:                         #wite for ESC key to exit
    #     cv2.destroyAllWindows()

def write_to_file(file_name, contours_dst):
    output_dir = "output_images/origin/" # 输出文件夹
    dst_img_address = output_dir + "Output__" + file_name
    cv2.imwrite(dst_img_address, contours_dst)

def main():
    # root_dir = 'images/'
    # entries = os.listdir(os.path.join(os.path.dirname(root_dir))
    img = load_image("0.png")
    contours, hierarchy = find_contours_sharpe(img)
    # The hierarchy returned by findContours has four columns : [Next, Previous, First_Child, Parent]
    # https://stackoverflow.com/questions/52397592/only-find-contour-without-child (How to get child )
    child_contour = hierarchy [0, :,2]
    cnts = contours
    # pirnt("number of contours:" + len(cnts))
    cnts = [ cnts[i] for i in child_contour if (cv2.contourArea(cnts[i]) > 100) and (cv2.contourArea(cnts[i]) < 1000)]
    for c in cnts:
        cX, cY = find_ceteroid_shape(c)
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
        draw_contour_and_centroid(img, c, cX, cY, (0,255,0), 3)

    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # write_to_file(i, contours_dst)

if __name__ == "__main__":
    main()
