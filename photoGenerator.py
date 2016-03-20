#!/usr/bin/python
#coding=utf-8

import os
import cv2
import time

def inspect_dir_existence():
	'''
	查看是否存在存储目录，不存在则创建。
	 :return 目录名
	'''
	img_dir =  os.path.dirname(os.path.abspath(__file__))+'/IMGDIR/'
	if os.path.isdir(img_dir) == False:
		os.mkdir(img_dir)
	return img_dir


def get_timestamp():
	return str(int(time.time()))


def call_camera(img_dir):
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
			cv2.imwrite(img_dir+timestamp+'.png',frame)
			print 'Have taken a photo named '+img_dir+timestamp+'.png'
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	img_dir = inspect_dir_existence()
	call_camera(img_dir)