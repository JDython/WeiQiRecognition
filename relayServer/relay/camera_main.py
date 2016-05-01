#!/usr/bin/python
#coding=utf-8

import os
import cv2
import time
import config
from chess_detection import *

def inspect_dir_existence():
	'''
	查看是否存在存储目录，不存在则创建。
	 :return 目录名
	'''
	img_dir  = getattr(config,'SAVE_IMG')
	#img_dir =  os.path.dirname(os.path.abspath(__file__))+'/IMGDIR/'
	if os.path.isdir(img_dir) == False:
		os.mkdir(img_dir)
	return img_dir


def get_timestamp():
	return str(int(time.time()))


def call_camera(img_dir):
	extension = getattr(config,'EXTENSION')
	# 0为先系统先找到的摄像头 1为后找到的
	cap = cv2.VideoCapture(0)
	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()
		# Our operations on the frame come here
		#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# Display the resulting frame
		cv2.imshow('frame',frame)
		k = cv2.waitKey(1)
		# wait for 'p' or 'q' key to save or exit
		if k & 0xFF == ord('q'):
			break
		elif k & 0xFF == ord('p'):
			timestamp = get_timestamp()
			resize_pic=cv2.resize(frame,(640,480),interpolation=cv2.INTER_CUBIC)
			cv2.imwrite(img_dir+timestamp+extension,resize_pic)
			print 'Have taken a photo named '+img_dir+timestamp+extension
			resize_pic,binary = img_pre_treatment(img_dir+timestamp+extension)
			vertical_lines,parallel_lines=get_chessboard_lines(binary)
			vertical_position,parallel_position = clipped_position(vertical_lines,parallel_lines)
			img_perspective=save_chessboard_img(resize_pic,vertical_position,parallel_position)
			save_clip_img()
			matrix_saver()
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	img_dir = inspect_dir_existence()
	call_camera(img_dir)