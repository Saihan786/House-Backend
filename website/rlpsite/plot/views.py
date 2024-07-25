from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse, HttpResponseRedirect

from .software import PlotOptimals, HRGenerator, LineFunctions, PolygonFunctions, RedLinePlot
# from .software import HRGenerator
from .software.PlotOptimals import plotProportions
from .forms import RegionForm



def index(request):
    template = loader.get_template("plot/index.html")

    return HttpResponse(template.render(context=None, request=request))


def generate(request):
    
    if request.method == "POST":
        form = RegionForm(request.POST)



        print(request.POST)
        
        
        
        
        
        
        if form.is_valid():
            return HttpResponseRedirect("/thanks/")
    else:
        form = RegionForm()


    return render(request, "plot/generate.html", {"form": form})