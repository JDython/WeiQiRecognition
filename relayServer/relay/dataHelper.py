#coding=utf-8

import os
import config

import random
import numpy as np

def search_last_img():
    extension = getattr(config,'EXTENSION')
    img_path = getattr(config,'SAVE_IMG')
    try:
        for root,dir,filename in os.walk(img_path):
            filename_list = [ int(i.split('.')[0]) for i in filename ]
        return str(max(filename_list))+extension
    except ValueError:
        return 'Fail: No Image To Be push!'

'''
以下为模拟棋局，仅测试使用。
'''

def dyadic_array_generator():
    dyadic_array =[]
    for i in range(19):
        dyadic_array.append([ random.randint(0,2)  for i in range(19)])
    return dyadic_array

if __name__ == '__main__':
    # last_img = search_last_img()
    # print last_img
    print dyadic_array_generator()
