from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse, HttpResponseRedirect

from .software.Main import startplot
from .forms import RegionForm, ExampleForm

import geopandas
import mpld3



def index(request):
    template = loader.get_template("plot/index.html")
    context = None
    
    # if request.method == "POST":
    #     form = ExampleForm()
    #     context = {"form": form}
    # else:
    #     form = ExampleForm()
    #     context = {"form": form}
    
    return HttpResponse(template.render(context=context, request=request))


def generate(request):
    if request.method == "POST":
        form = RegionForm(request.POST, request.FILES)
        context = {"form": form}
        
        if form.is_valid():
            file = request.FILES["regionfile"].file
            rlp = geopandas.read_file(file)
            fig = startplot(rlp)

            mp = mpld3.plugins.MousePosition(fontsize=12, fmt='.6g')
            mpld3.plugins.connect(fig, mp)
            context["graph"] = mpld3.fig_to_html(fig)

            return render(request, "plot/generate.html", context)
        else:
            return HttpResponse("error with invalid form")

    else:
        form = RegionForm()
        context = {"form": form}

        return render(request, "plot/generate.html", context)
