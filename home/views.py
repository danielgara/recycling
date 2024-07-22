from django.shortcuts import render


def index(request):
    viewData = {}
    viewData["title"] = "Recycling App"
    return render(request, 'home/index.html', {"viewData": viewData})


def about(request):
    viewData = {}
    viewData["title"] = "About us"
    viewData["breadcrumbItems"] = [
        {"name": "Home", "route": "home.index"},
        {"name": "About", "route": "home.about"},
    ]
    return render(request, 'home/about.html', {"viewData": viewData})


def learn(request):
    viewData = {}
    viewData["title"] = "Learn"
    viewData["breadcrumbItems"] = [
        {"name": "Home", "route": "home.index"},
        {"name": "Learn", "route": "home.learn"},
    ]
    return render(request, 'home/learn/index.html', {"viewData": viewData})


def l1(request):
    viewData = {}
    viewData["title"] = "Level 1"
    viewData["breadcrumbItems"] = [
        {"name": "Home", "route": "home.index"},
        {"name": "Learn", "route": "home.learn"},
        {"name": "Level 1", "route": "home.learn.l1"},
    ]
    return render(request, 'home/learn/l1.html', {"viewData": viewData})


def l2(request):
    viewData = {}
    viewData["title"] = "Level 2"
    viewData["breadcrumbItems"] = [
        {"name": "Home", "route": "home.index"},
        {"name": "Learn", "route": "home.learn"},
        {"name": "Level 2", "route": "home.learn.l2"},
    ]
    return render(request, 'home/learn/l2.html', {"viewData": viewData})


def l3(request):
    viewData = {}
    viewData["title"] = "Level 3"
    viewData["breadcrumbItems"] = [
        {"name": "Home", "route": "home.index"},
        {"name": "Learn", "route": "home.learn"},
        {"name": "Level 3", "route": "home.learn.l3"},
    ]
    return render(request, 'home/learn/l3.html', {"viewData": viewData})


def experience(request):
    viewData = {}
    viewData["title"] = "Registro de Experiencia"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Registro de Experiencia", "route": "home.experience"},
    ]
    return render(request, 'home/experience.html', {"viewData": viewData})
