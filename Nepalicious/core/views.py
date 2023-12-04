from django.shortcuts import render

# Create your views here.
def index(request):
    # DISPLAY PHOTO
    return render(request, "landingPage/index.html")
