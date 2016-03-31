#coding=utf-8

import os
import config

def search_last_img():
    extension = getattr(config,'EXTENSION')
    img_path = getattr(config,'SAVE_IMG')
    for root,dir,filename in os.walk(img_path):
        filename_list = [ int(i.split('.')[0]) for i in filename ]
    return str(max(filename_list))+extension

if __name__ == '__main__':
    last_img = search_last_img()
    print last_img