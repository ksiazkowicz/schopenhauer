from django.shortcuts import render


def homepage_view(request, template="site/home.html"):
    return render(request, template, locals())
