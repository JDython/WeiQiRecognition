#coding=utf-8

import math
import numpy as np
import cv2
import cv2.cv as cv

im = cv2.imread('chessboard.jpg')
resize_pic=cv2.resize(im,(640,480),interpolation=cv2.INTER_CUBIC)
resize_pic = im
resize_pic = cv2.GaussianBlur(resize_pic,(5,5),0)
gray = cv2.cvtColor(resize_pic,cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray,60,255,cv2.THRESH_BINARY)


cv2.imshow("img", binary)
k = cv2.waitKey(0) & 0xFF
if k == 27:
    cv2.destroyAllWindows()
edges = cv2.Canny(binary,50,100)
lines_data = cv2.HoughLines(edges,1,np.pi/180,80)


parallel_theta = []
vertical_theta = []
for rho,theta in lines_data[0]:
    print 'rho:  '+str(rho)+'theta:  '+str(theta)
    if 2>theta > 1:
        vertical_theta.append([theta,rho])
    elif theta < 1 :
        parallel_theta.append([theta,rho])
    elif theta>3:
        parallel_theta.append([theta,rho])

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

vertical_position = sorted(chessboard_position[0:2],key=lambda x: x[0])
parallel_position = sorted(chessboard_position[2::],key=lambda x: x[0])
print '-------------'
print vertical_position
print parallel_position


chess_vertical_distence = abs(vertical_position[1][0] - vertical_position[0][0])/18
chess_parallel_distence = abs(parallel_position[0][1] - vertical_position[0][1])/18
print chess_vertical_distence,chess_parallel_distence

vertical_position[0][0] = vertical_position[0][0]-chess_vertical_distence/2
vertical_position[0][1] = vertical_position[0][1]-chess_vertical_distence/2
vertical_position[1][0] = vertical_position[1][0]+chess_vertical_distence/2
vertical_position[1][1] = vertical_position[1][1]-chess_vertical_distence/2

parallel_position[0][0] = parallel_position[0][0]-chess_parallel_distence/2
parallel_position[0][1] = parallel_position[0][1]+chess_parallel_distence/2
parallel_position[1][0] = parallel_position[1][0]+chess_parallel_distence/2
parallel_position[1][1] = parallel_position[1][1]+chess_parallel_distence/2



#img=cv2.imread('chessboard.jpg')
pts3 = np.float32([vertical_position[0],vertical_position[1],parallel_position[0],parallel_position[1]])
pts4 = np.float32([[0,0],[640,0],[0,480],[640,480]])
M_perspective = cv2.getPerspectiveTransform(pts3,pts4)
img_perspective = cv2.warpPerspective(resize_pic, M_perspective, (0, 0))

cv2.imwrite('crop.jpg',img_perspective)
img=cv.LoadImage('crop.jpg')


#marking clipped position
# for i in range(19):
#     for j in range(19):
#         cv2.rectangle(img_perspective,(0+int(33.68*i),int(25.26*j)),(int(33.68*(i+1)),int(25.26*(j+1))),(0,255,0),1)

vertical_distance_decimal,vertical_distance_integer = math.modf(float(640)/19)
parallel_distance_decimal,parallel_distance_integer = math.modf(float(480)/19)
print vertical_distance_decimal,vertical_distance_integer,parallel_distance_decimal,parallel_distance_integer

for i in range(19):
    for j in range(19):
        wn_position =(int(vertical_distance_integer*i)+int(vertical_distance_decimal*i),int(parallel_distance_integer*j)+int(parallel_distance_decimal*j))
        es_position =(int(vertical_distance_integer*(i+1)+int(vertical_distance_decimal*i)),int(parallel_distance_integer*(j+1))+int(parallel_distance_decimal*j))
        cv2.rectangle(img_perspective,wn_position,es_position,(0,255,0),1)
        img_backup=cv.CloneImage(img)
        cv.SetImageROI(img_backup,(wn_position[0],wn_position[1],33,25))
        cv.SaveImage('ClippedImg/%d_%d.jpg'%(i,j),img_backup)



cv2.imwrite('crop2.jpg',img_perspective)
cv2.imshow('crop',img_perspective)
k = cv2.waitKey(0) & 0xFF
if k == 27:
    cv2.destroyAllWindows()

