from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse
# from . import 

import webbrowser
import os


def index(request):
    embedmap = loader.get_template("plot/map.html")
    template = loader.get_template("plot/index.html")
    context = {
        "map": embedmap,
    }



    


    

    return HttpResponse(template.render(context=context, request=request))