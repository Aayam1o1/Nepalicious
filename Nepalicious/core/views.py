from django.shortcuts import render

# Create your views here.
def index(request):
    # DISPLAY PHOTO
    return render(request, "landingPage/index.html")

def error_404(request, exception):

    return render(request, '404.html', status=404)
 
def error_500(request):
    return render (request, '404.html', status=500)