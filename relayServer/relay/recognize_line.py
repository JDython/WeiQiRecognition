#!/usr/bin/python
#coding=utf-8

import config
import cv2
import numpy as np


def lineRecognizer(path):
	'''
    :param path 带识别图片的路径
	:returns lines_data 识别出的直线数据；resize_pic 修改后的图片
	'''
	img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
	resize_pic=img
	#resize_pic=cv2.resize(img,(640,480),interpolation=cv2.INTER_CUBIC)
	edges = cv2.Canny(resize_pic,50,150)
	lines_data = cv2.HoughLines(edges,1,np.pi/180,150)
	return lines_data,resize_pic


def drawLines(lines_data,pic):
	'''
	横线rho为正，竖线为负。theta均为0；
	:param lines_data:
	:param pic:
	:return: rho列表
	'''
	line_para=[]
	for rho,theta in lines_data[0]:
		print 'rho:  '+str(rho)+'theta:  '+str(theta)
		line_para.append(rho)
		a = np.cos(theta)
		b = np.sin(theta)
		x0 = a*rho
		y0 = b*rho
		x1 = int(x0 + 1000*(-b))
		y1 = int(y0 + 1000*(a))
		x2 = int(x0 - 1000*(-b))
		y2 = int(y0 - 1000*(a))
		cv2.line(pic,(x1,y1),(x2,y2),(255,0,0),2)
		cv2.imshow('image',pic)
		k = cv2.waitKey(0) & 0xFF
		if k == 27:
			cv2.destroyAllWindows()
	return line_para

if __name__ == '__main__':
	path=config.TO_BE_RECOGNIZED_IMG_PATH+config.TO_BE_RECOGNIZED_IMG
	lines_data,resize_pic = lineRecognizer(path)
	drawLines(lines_data,resize_pic)
