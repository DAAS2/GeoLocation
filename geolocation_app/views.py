from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from .models import User, Parent, Child, ChatMessage
def index(request):
    parent = None
    children = None
    is_child = False
    parent_id = None
    message = None

    if request.user.is_authenticated:
        try:
            parent = Parent.objects.get(user=request.user)
            children = Child.objects.filter(parent=parent)
            parent_id = parent.id
        except Parent.DoesNotExist:
            try:
                child = Child.objects.get(user=request.user)
                parent = child.parent
                children = [child]
                is_child = True
            except Child.DoesNotExist:
                pass

    return render(request, 'geolocation_app/index.html', {
        'parent': parent,
        'children': children,
        'is_child': is_child,
        'parent_id': parent_id,
        'message': message  
    })


def find_child(request):
    try:
        child = Child.objects.get(user=request.user)
    except Child.DoesNotExist:
        child = None
        
    return render(request, "geolocation_app/findchild.html", {
        'child': child
    })



@require_POST
@csrf_exempt
def save_child_location(request):
    if request.user.is_authenticated and request.body:
        try:
            data = json.loads(request.body)
            lat = data.get('lat')
            lng = data.get('lng')
            child = Child.objects.get(user=request.user)
            child.latitude = lat
            child.longitude = lng
            child.save()
            return JsonResponse({'success': True, 'lat': lat, 'lng': lng})
        except (Child.DoesNotExist, json.JSONDecodeError):
            return JsonResponse({'success': False, 'message': 'Invalid request or Child not found'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

def contact_child(request, *args, **kwargs):
    parent = None
    children = None
    is_child = False
    
    if request.user.is_authenticated:
        try:
            parent = Parent.objects.get(user=request.user)
            children = Child.objects.filter(parent=parent)
        except Parent.DoesNotExist:
            try:
                # If the user is not a parent, try to get their child instance
                child = Child.objects.get(user=request.user)
                parent = child.parent
                children = [child]
                is_child = True
            except Child.DoesNotExist:
                # If the user is neither parent nor child, handle accordingly
                pass
    
    # Fetch last messages
    last_messages = ChatMessage.objects.all()
    
    context = {
        "user": request.user,
        "children": children,
        "parent": parent,
        "last_messages": last_messages
    }
    return render(request, "geolocation_app/contact_child.html", context)



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "geolocation_app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "geolocation_app/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        accounttype = request.POST["Type"]
        phone = request.POST.get("phone_number")
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "geolocation_app/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            
            if accounttype == ("parent"):
                parent = Parent.objects.create(user=user, phone_number=phone)
                parent.save()
                
            elif accounttype == ("child"):
                parent_id = request.POST["parent_id"]
                parent = Parent.objects.get(id=parent_id)
                child = Child.objects.create(user=user, parent=parent)
                child.save()
                
        except IntegrityError:
            return render(request, "geolocation_app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "geolocation_app/register.html")
