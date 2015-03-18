from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

def index(request):
    cat = Category.objects.order_by('-likes')[:5]
    pag = Page.objects.order_by('-likes')[:5]
    context_dict = {'categories':cat,'pages':pag}
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return HttpResponse("Rango says here is the about page.<br><a href='/rango/'>Index</a>")

def category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form':form})

def add_page(request):
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = PageForm()

    return render(request, 'rango/add_page.html', {'form':form})
