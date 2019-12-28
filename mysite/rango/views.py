from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    #  to the template rendering engine.
    context_dict = {}
    try:
        # Can we find a category name slug with the given name?
        #  If we can't, the .get() method raises a DoesNotExist exception.
        #  So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)


        # Retrieve all of the associated pages.
        #  Note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        #  We also add the category object from
        #  the database to the context dictionary.
        #  We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
            context_dict['category'] = None
            context_dict['pages'] = None
    return render(request, 'rango/category.html', context_dict)


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    return render(request, 'rango/index.html', context=context_dict)

# def about(request):
#     return HttpResponse("Hello World!<a href='/rango/'>Index</a>")
def about(request):
    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)
    return render(request, 'rango/about.html', {})

def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form })

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
            else:
                print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)



