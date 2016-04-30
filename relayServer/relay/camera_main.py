#coding=utf-8

from matrix_generator import *
from chess_detection import *

resize_pic,binary = img_pre_treatment('static/IMGDIR/ichessboard5.jpg')
vertical_lines,parallel_lines=get_chessboard_lines(binary)
vertical_position,parallel_position = clipped_position(vertical_lines,parallel_lines)
img_perspective=save_chessboard_img(resize_pic,vertical_position,parallel_position)
save_clip_img()

matrix_saver()