from django.urls import reverse
from django.shortcuts import redirect

class RedirectAuthenticatedUserMiddleware():
    def __init__(self,get_response):
        self.get_response = get_response
    

    def __call__(self, request):

        #user logined or not 
        if request.user.is_authenticated:
            #list of path to check
            path_to_redirect=[reverse('blog:login'),reverse('blog:register')]
            if request.path in path_to_redirect:
                return redirect(reverse('blog:index'))
            
        response = self.get_response(request)
        return response
    
class RestrictUnauthenticatedUserMiddleware():
    def __init__(self,get_response):
        self.get_response =get_response

    def __call__(self, request):
        restricted_path=[reverse('blog:dashboard')]
        if not request.user.is_authenticated and request.path in restricted_path:
                return redirect(reverse('blog:login'))
        
        response = self.get_response(request)
        return response
