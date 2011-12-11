from django.shortcuts import  render, render_to_response
from game import views

def base(request):
    if request.user.is_authenticated():
        return views.start(request)
    else:
        return render(request, 'login.html')
