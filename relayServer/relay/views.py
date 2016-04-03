import config
import dataHelper
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def relay(request):
    # img_path = getattr(config,'DJANGO_STATIC_PATH')
    # last_img_name = getattr(dataHelper,'search_last_img')()
    # if request.is_ajax() and request.method == 'GET':
    #     return JsonResponse(img_path+last_img_name, safe=False)
    # return render(request,'weiqi.html',{'imgPath':img_path+last_img_name})

    dyadic_array = dataHelper.dyadic_array_generator()
    if request.is_ajax() and request.method == 'GET':
        return JsonResponse(dyadic_array, safe=False)
    return render(request,'weiqi.html',{'dyadic_array':dyadic_array})