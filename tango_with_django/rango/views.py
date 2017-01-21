from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm,UserProfileForm

def index(request):

    category_list = Category.objects.order_by("-likes")[:5]
    page_list = Page.objects.order_by("-views")[:5]
    context_dict = {"categories":category_list, "pages":page_list}
    return render(request, "rango/index.html", context = context_dict)
    
def about(request):
    context_dict = {}
    return render(request, "rango/about.html", context = context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict["pages"] = pages
        context_dict["category"] = category
    except Category.DoesNotExist:

        context_dict["category"] = None
        context_dict["page"] = None

    return render(request, "rango/category.html", context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, "rango/add_category.html",{"form":form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {"form":form, "category":category}
    return render(request, "rango/add_page.html", context_dict)

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            

            #set new password
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            
            profile.save()

            registered = True

        else:
            #Form invalid
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    context_dict = {"user_form":user_form,"profile_form":profile_form,
                    "registered":registered}
    #print user_form
    return render(request,"rango/register.html",context_dict)

def user_login(request):
    

    if request.method == "POST":
        #get credentials
        username = request.POST.get("username")
        password = request.POST.get("password")

        #check credentials
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                #user credentials correct and user is active so login
                login(request, user)
                return HttpResponseRedirect("/rango/")
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid ligin details: {0}, {1}".format(username,password)
            return HttpResonse("Invalid login details supplied.")

    else:
        return render(request, "rango/login.html",{})

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/rango/")
                  
