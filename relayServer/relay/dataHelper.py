#coding=utf-8

import os
import config
from models import *
from django.db.models.query import QuerySet


def search_last_img():
    extension = getattr(config,'EXTENSION')
    img_path = getattr(config,'SAVE_IMG')
    try:
        for root,dir,filename in os.walk(img_path):
            filename_list = [ int(i.split('.')[0]) for i in filename ]
        return str(max(filename_list))+extension
    except ValueError:
        return 'Fail: No Image To Be push!'


def serialize_objects(django_objects,class_models,*args):
    '''
    models 序列化
    :param django_objects:
    :param args:
    :param class_models:name of models class
    :return:json
    '''
    serialize_list = []
    if isinstance(django_objects,QuerySet):
        for django_object in django_objects:
            data_dic = {}
            for column in args:
                data_dic[column]= str(eval('django_object.%s'%column))
            serialize_list.append(data_dic)
    if isinstance(django_objects,class_models):
        data_dic = {}
        for column in args:
            data_dic[column]= str(eval('django_objects.%s'%column))

        serialize_list.append(data_dic)
    return serialize_list


def get_lastest_matrix():
    try:
        lastest_matrix_object = chess_composition.objects.all()[0]
    except IndexError:
        return None
    return serialize_objects(lastest_matrix_object,chess_composition,'id','time','matrix')



if __name__ == '__main__':
    # last_img = search_last_img()
    # print last_img
    #print dyadic_array_generator()
    lastest_matrix_object = get_lastest_matrix()
    serialize_objects(lastest_matrix_object,chess_composition,'id','time','matrix')

