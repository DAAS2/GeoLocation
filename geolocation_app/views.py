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
        parent = Parent.objects.get(user=request.user)
        child = Child.objects.filter(parent=parent)
    except Child.DoesNotExist:
        pass
        
    return render(request, "geolocation_app/findchild.html", {
        'child': child
    })
    

@csrf_exempt
def update_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            # Assuming the child is associated with user
            child = Child.objects.get(user=request.user)
            child.latitude = latitude
            child.longitude = longitude
            child.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



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
        "is_child": is_child,
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
                try: 
                    parent_id = request.POST["parent_id"]
                    parent = Parent.objects.get(id=parent_id)
                    child = Child.objects.create(user=user, parent=parent)
                    child.save()
                except Parent.DoesNotExist:
                    return render(request, "geolocation_app/register.html", {
                        "message": "Parent does not have that ID."
                    })
                

        except IntegrityError:
            return render(request, "geolocation_app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "geolocation_app/register.html")
