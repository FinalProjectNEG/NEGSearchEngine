from django.shortcuts import render, redirect
from .models import Product
from .Search import Search

def home(request):
    return render(request,'searchpage/home.html')

def search_page(request):

    data = request.POST.get('search')
    print(data)
    object_search = Search(data)
    if object_search != "not found":
        results = object_search.Start_search()
    else:
        print("jjjjjjjjjjjjj")
        results = "not found"
    return render(request,'searchpage/search.html',{"dic":results,"data":data})

def repeat(request):
    data = request.POST.get('search')
    print(data)
    object_search = Search(data)
    if object_search != "not found":
        results = object_search.Start_search()
    else:
        results = "not found"
    return render(request,'searchpage/search.html',{"dic":results,"data":data})


def mong(request):
    obj = Product.objects.get(id=1)
    context = {
        'title':obj.title,
        'description':obj.descriptio
    }
    return render(request,"product/detail.html",context)

