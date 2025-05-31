from django.shortcuts import render
def custom_pag_not_found(request,exception):
    return render(request,'pageNotFound.html',status=404)