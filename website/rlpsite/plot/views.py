from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse

from ....software import HRGenerator



def index(request):
    template = loader.get_template("plot/index.html")

    return HttpResponse(template.render(context=None, request=request))