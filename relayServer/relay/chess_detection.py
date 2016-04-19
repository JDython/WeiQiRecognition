#coding=utf-8

import numpy as np
import cv2

im = cv2.imread('chessboard.jpg')
#resize_pic=cv2.resize(im,(640,480),interpolation=cv2.INTER_CUBIC)
resize_pic = im
gray = cv2.cvtColor(resize_pic,cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray,45,255,cv2.THRESH_BINARY)


cv2.imshow("img", resize_pic)
k = cv2.waitKey(0) & 0xFF
if k == 27:
    cv2.destroyAllWindows()
edges = cv2.Canny(binary,50,150)
lines_data = cv2.HoughLines(edges,1,np.pi/180,130)


parallel_theta = []
vertical_theta = []
for rho,theta in lines_data[0]:
    print 'rho:  '+str(rho)+'theta:  '+str(theta)
    if 2>theta > 1:
        vertical_theta.append([np.pi/2,rho])
    elif theta < 1 :
        parallel_theta.append([0,rho])
    elif theta>3:
        parallel_theta.append([np.pi,rho])

    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(edges,(x1,y1),(x2,y2),(255,0,0),2)
    cv2.imshow('image',edges)
    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()

vertical_theta=sorted(vertical_theta,key=lambda x: x[1])
parallel_theta=sorted(parallel_theta,key=lambda x: x[1])
# print sorted(vertical_theta,key=lambda x: x[1])
# print sorted(parallel_theta,key=lambda x: x[1])


def init_equation_param(ver_lines_param,par_lines_param):
    theta_ratio = []
    rho_ratio = []
    theta_ratio.append([np.cos(ver_lines_param[0]),np.sin(ver_lines_param[0])])
    theta_ratio.append([np.cos(par_lines_param[0]),np.sin(par_lines_param[0])])
    rho_ratio.append(ver_lines_param[1])
    rho_ratio.append(par_lines_param[1])
    return theta_ratio,rho_ratio



def solve_equation(a,b):
    '''
    解二元一次方程组：如 3 * x0 + x1 = 9 and x0 + 2 * x1 = 8
    直线的参数方程为： x *cos(theta) + y * sin(theta)  = r
    :param a:np.array([[3,1], [1,2]])
    :param b:np.array([9,8])
    :return:np.linalg.solve(a, b)
    '''
    a=np.array(a)
    b=np.array(b)
    return np.linalg.solve(a,b)

def solve_position(ver_lines_param_list,par_lines_param_list):
    position_list = []
    for ver_lines_param in ver_lines_param_list:
        for par_lines_param in par_lines_param_list:
            #print ver_lines_param,par_lines_param
            theta_ratio,rho_ratio = init_equation_param(ver_lines_param,par_lines_param)
            position_list.append(list(solve_equation(theta_ratio,rho_ratio)))
    return position_list

chessboard_position = solve_position([vertical_theta[0],vertical_theta[-1]],[parallel_theta[0],parallel_theta[-1]])
#print chessboard_position
vertical_position = sorted(chessboard_position[0:2],key=lambda x: x[0])
parallel_position = sorted(chessboard_position[2::],key=lambda x: x[0])
print '-------------'
print vertical_position
print parallel_position



img=cv2.imread('chessboard.jpg')

vertical_distence = abs(vertical_position[1][0] - vertical_position[0][0])/18
parallel_distence = abs(parallel_position[0][1] - vertical_position[0][1])/18
print vertical_distence,parallel_distence

for i in range(19):
    for j in range(19):
        if i<9:
            cv2.circle(img,(int(vertical_position[0][0]+vertical_distence*i),int(vertical_position[0][1]+parallel_distence*j)),12,(55,255,155),1)
            centre_position = int(((vertical_position[1][0]-vertical_distence*i) -(vertical_position[0][0]+vertical_distence*i))/2)
        elif i==9:
            cv2.circle(img,(552-23*(i-1)-centre_position,27+int(parallel_distence*j)),12,(55,255,155),1)
        else:
            cv2.circle(img,(552-int(vertical_distence*(18-i)),27+int(parallel_distence*j)),12,(55,255,155),1)

#crop_chessboard=img[14:39, 120:145]
cv2.imshow('crop',img)

k = cv2.waitKey(0) & 0xFF
if k == 27:
    cv2.destroyAllWindows()

