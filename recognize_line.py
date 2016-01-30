#!/usr/bin/python

import cv2
import numpy as np

pic_name = 'three_lines.jpg'
line_num=0
raw_line_data =[]
del_line_data = []
img = cv2.imread(pic_name,cv2.IMREAD_GRAYSCALE)
res=cv2.resize(img,(640,480),interpolation=cv2.INTER_CUBIC)
res=cv2.GaussianBlur(res,(5,5),0)
edges = cv2.Canny(res,50,150)
lines = cv2.HoughLines(edges,1,np.pi/180,180)


for rho,theta in lines[0]:
	raw_line_data.append((rho,theta))
	del_line_data.append((rho,theta))
	print 'rho:  '+str(rho)+'theta:  '+str(theta)
	line_num +=1
	a = np.cos(theta)
	b = np.sin(theta)
	x0 = a*rho
	y0 = b*rho
	x1 = int(x0 + 1000*(-b))
	y1 = int(y0 + 1000*(a))
	x2 = int(x0 - 1000*(-b))
	y2 = int(y0 - 1000*(a))
	cv2.line(res,(x1,y1),(x2,y2),(0,0,255),2)
	cv2.imshow('image',res)
	k = cv2.waitKey(0) & 0xFF
	if k == 27:
		cv2.destroyAllWindows()


IGNORE_ERROR = 15
line_data =[]

for i in raw_line_data:
	temp_line_data =[]
	max_rho_error = i[0]+IGNORE_ERROR
	min_rho_error = i[0]-IGNORE_ERROR
	max_theta_error = i[1]+IGNORE_ERROR
	min_theta_error = i[1]-IGNORE_ERROR
	for item in del_line_data:
		if min_rho_error<item[0]<max_rho_error and min_theta_error<item[1]<max_theta_error:
			temp_line_data.append(del_line_data.pop(del_line_data.index(item)))

	if len(temp_line_data):
		total_rho =0
		total_theta =0
		length = len(temp_line_data)
		for num in range(length):
			total_rho +=temp_line_data[num][0]
			total_theta+=temp_line_data[num][1]
		line_data.append((total_rho/length,total_theta/length))
#print line_data
print 'The number of lines is '+str(len(line_data))
