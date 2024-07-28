from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse, HttpResponseRedirect

from .software.PlotOptimals import startplot
from .forms import RegionForm

import geopandas
import mpld3






def index(request):
    template = loader.get_template("plot/index.html")

    return HttpResponse(template.render(context=None, request=request))


def generate(request):
    if request.method == "POST":
        form = RegionForm(request.POST, request.FILES)
        context = {"form": form}
        
        if form.is_valid():
            file = request.FILES["regionfile"].file
            rlp = geopandas.read_file(file)
            fig, houses = startplot(rlp)

            # fig, ax = plt.subplots()
            # points = ax.plot(range(10), 'o')
            # labels = ['<h1>{title}</h1>'.format(title=i) for i in range(10)]
            # plugins.connect(fig, plugins.PointHTMLTooltip(points, labels))

            # gc = GeometryCollection(houses)
            # labels = ['<h1>{title}</h1>'.format(title=i) for i in range(350)]
            # plugins.connect(fig, plugins.PointHTMLTooltip(gc, labels))


            # df = geopandas.GeoDataFrame()
            # df.price = 
            # fig, ax = plt.subplots()
            # axes = df.price.plot(ax=ax, ls='', marker='.')
            # labels = df.labels.values()
            # tooltip = mpld3.plugins.PointLabelTooltip(axes.get_lines()[0], labels=labels)
            # mpld3.plugins.connect(fig, tooltip)


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
