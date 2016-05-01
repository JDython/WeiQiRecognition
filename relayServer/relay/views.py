import dataHelper
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def relay(request):
    matrix_data = dataHelper.get_lastest_matrix()
    matrix_data[0]['matrix'] = eval(matrix_data[0]['matrix'])
    print matrix_data
    if request.is_ajax() and request.method == 'GET':
        return JsonResponse(matrix_data, safe=False)
    return render(request,'weiqi.html',{'matrix_data':matrix_data})