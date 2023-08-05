from django.shortcuts import redirect

class RestrictEmployerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and user.customer.employer:
            if request.path == '/' or request.path.startswith('/jview/'):  # Update this with the actual URL of your home page
                return redirect('cview')
        response = self.get_response(request)
        return response
    
class RestrictEmployeeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and not user.customer.employer:
            if request.path == '/cview/' or request.path.startswith('/cjview/') or request.path == '/create_job/':  # Update this with the actual URL of your home page
                return redirect('home')
        response = self.get_response(request)
        return response

class RestrictunauthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if not user.is_authenticated :
            if request.path == '/cview/'or request.path == '/upload_resume/' or request.path.startswith('/cjview/') or request.path.startswith('/apply/') or request.path == '/create_job/':  # Update this with the actual URL of your home page
                return redirect('home')
        response = self.get_response(request)
        return response
    
        
