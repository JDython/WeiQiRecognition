#coding=utf-8

import numpy as np
import cv2
import os


def find_picture(img_path):
    file_path_list =[]
    label_list= []
    for root,dir,filenames in os.walk(img_path):
        for filename in filenames:
            file_path_list.append(root+filename)
            label_list.append(int(filename.split('_')[0]))
    return file_path_list,np.array(label_list)[:,np.newaxis]


def preprocess_img(filename_list):
    preprocess_file_list = []
    for filename in filename_list:
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        preprocess_file_list.append(gray)
    preprocess_file_list = np.array(preprocess_file_list).reshape(-1,12100).astype(np.float32)
    return preprocess_file_list

def img_threshold():
    img = cv2.imread('chessboard1.jpg',0)
    resize_pic=cv2.resize(img,(640,480),interpolation=cv2.INTER_CUBIC)
    resize_pic = cv2.medianBlur(resize_pic,5)
    th2 = cv2.adaptiveThreshold(resize_pic,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
cv2.THRESH_BINARY,11,2)
    #ret,thresh1 = cv2.threshold(resize_pic,127,255,cv2.THRESH_BINARY)
    cv2.imshow('image',th2)
    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    train_filename_list,train_label_list=find_picture('train/')
    train_file_list = preprocess_img(train_filename_list)


    test_filename_list,test_label_list=find_picture('test/')
    test_file_list = preprocess_img(test_filename_list)

    knn = cv2.KNearest()
    knn.train(train_file_list,train_label_list)
    ret,result,neighbours,dist = knn.find_nearest(test_file_list,k=2)

    matches = result==test_label_list
    correct = np.count_nonzero(matches)
    accuracy = correct*100.0/result.size
    print accuracy
   # img_threshold()


