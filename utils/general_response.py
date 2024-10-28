from venv import logger
from django.http import JsonResponse
from rest_framework.response import Response



def handler404(request, exception):
    
        return JsonResponse({
        'status' : False,
        'errorNum' : 404,
        'Message' : 'Path Not Found'
    }, status = 404)

def handler500(request):
     return JsonResponse({
        'status' : False,
        'errorNum' : 404,
        'Message' : 'Internal Server Error'
    }, status = 500)
     
def handler401(request, exception):
    
        return JsonResponse({
        'status' : False,
        'errorNum' : 401,
        'Message' : 'Unauthorized'
    }, status = 401)

def success_response(status_code, message = 'Success', data = None):
    response_data = {
        'status' : True,
        'errorNum' : None,
        'Message' : message
    }
    if data:
        response_data.update(data)
    return Response(response_data, status_code)
    

def error_response(error_number, message, status_code):
    return Response({
        'status' : False,
        'errorNum' : error_number,
        'Message' : message
    }, status_code)
    