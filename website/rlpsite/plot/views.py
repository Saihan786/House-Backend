from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse, HttpResponseRedirect

from .software.PlotOptimals import startplot, example
from .forms import RegionForm

from io import StringIO
import geopandas



def index(request):
    template = loader.get_template("plot/index.html")

    return HttpResponse(template.render(context=None, request=request))


def generate(request):
    data = None
    
    if request.method == "POST":
        form = RegionForm(request.POST, request.FILES)
        
        if form.is_valid():
            print(":D")
            
            file = request.FILES["regionfile"].file
            rlp = geopandas.read_file(file)
            fig, plot = startplot(rlp)
            
            imgdata = StringIO()
            fig.savefig(imgdata, format='svg')
            imgdata.seek(0)

            data = imgdata.getvalue()
            
    else:
        form = RegionForm()


    return render(request, "plot/generate.html", {"form": form, "graph": data})