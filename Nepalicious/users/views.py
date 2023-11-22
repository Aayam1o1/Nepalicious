from django.shortcuts import render

# Create your views here.
# REGISTER
def registerUser(request):
    
    return render(request, 'login-Register/register.html')