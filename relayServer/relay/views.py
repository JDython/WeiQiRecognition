import dataHelper
from models import *
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def relay(request):
    with open('relay/static/chessboard_position.txt','r') as f:
        matrix = eval(f.readlines()[0])
    if request.is_ajax() and request.method == 'GET':
        return JsonResponse(matrix, safe=False)
    return render(request,'weiqi.html',{'dyadic_array':matrix})