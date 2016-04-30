#coding=utf-8

import re
import cv2

import train
import config


def init_matrix():
    chessboard_matrix = []
    for i in range(19):
        chessboard_matrix.append([ 0  for j in range(19)])
    return chessboard_matrix


def get_matrix():
    chessboard_matrix=init_matrix()
    train_filename_list,train_label_list=train.find_picture('static/train/')
    train_file_list = train.preprocess_img(train_filename_list)

    test_filename_list,test_label_list=train.find_picture('static/ClippedImg/')
    test_file_list = train.preprocess_img(test_filename_list)

    knn = cv2.KNearest()
    knn.train(train_file_list,train_label_list)
    ret,result,neighbours,dist = knn.find_nearest(test_file_list,k=3)
    for i in  range(len(result)):
        #print int(result[i][0]),test_filename_list[i]
        if int(result[i][0]) ==1:
            position = re.search(r'\d{1,2}_\d{1,2}',str(test_filename_list[i])).group().split('_')
            xposition,yposition = int(position[0]),int(position[1])
            chessboard_matrix[xposition][yposition]=1
        if int(result[i][0]) ==2:
            position = re.search(r'\d{1,2}_\d{1,2}',str(test_filename_list[i])).group().split('_')
            xposition,yposition = int(position[0]),int(position[1])
            chessboard_matrix[xposition][yposition]=2
        # if str(test_filename_list[i]).find('2_2') != -1:
        #     print result[i],test_filename_list[i]
    return chessboard_matrix

def matrix_saver():
    file_path='static/chessboard_position.txt'
    print file_path
    with open(file_path,'w') as f:
        f.write(str(get_matrix()))



if __name__ == '__main__':
    #print get_matrix()
    matrix_saver()