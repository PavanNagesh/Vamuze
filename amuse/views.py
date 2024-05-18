# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import User
from django.db import connection
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
import time
from django.conf import settings
from datetime import datetime, timedelta
from django.core.mail import send_mail
import random
from django.http import HttpResponseForbidden


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signin')
        
        # Check if the email or username already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already used.')
            return redirect('signin')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('signin')
        
        try:
            # Create a new user instance and save it to the database
            user = User.objects.create(username=username, email=email, password=password)
            messages.success(request, 'You are now registered and can log in.')
            return redirect('login')  # Redirect to the login page after successful sign-up
        except IntegrityError:
            messages.error(request, 'An error occurred while saving your data. Please try again.')
            return redirect('signin')
            
    return render(request, 'signin.html')

from django.shortcuts import render, redirect
from django.utils import timezone
from django.db import connection
from django.contrib.auth import login as auth_login
from .models import User

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        query = f"SELECT * FROM amuse_user WHERE username = '{username}' AND password = '{password}'"

        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

        if row:
            user = User.objects.get(username=username)
            user.last_login = timezone.now()
            user.save()

            # Log the user in using Django's login function
            auth_login(request, user)
            return redirect('index')

        return render(request, 'login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')

@csrf_exempt
def user_profile(request):
    # Assuming user is already authenticated
    # You can access user's details via request.user
    return render(request, 'userprofile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to your login page URL


def index(request):
    return render(request, 'index.html')

def innerpage(request):
    return render(request, 'innerpage.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def header(request):
    return render(request, 'header.html')

def footer(request):
    return render(request, 'footer.html')

def services(request):
    return render(request, 'services.html')

def home(request):
    return render(request, 'home.html')


@login_required
@csrf_exempt
def change(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        # Update user's email in the database
        request.user.email = new_email
        request.user.save()
        return redirect('userprofile')  # Redirect to the user profile page after updating the email
    return render(request, 'change.html')  # Render the change email page

def safety(request):
    return render(request, 'safety.html')

def rules(request):
    return render(request, 'rules.html')

@login_required
@csrf_exempt
def update(request):
    # Handle form submission via POST request
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        
        # Retrieve the current user
        user = request.user
        
        # Update the user's username
        if new_username:
            user.username = new_username
        
        # Update the user's email
        if new_email:
            user.email = new_email
        
        # Save the updated user data
        user.save()
        
        # Provide feedback to the user
        messages.success(request, "Profile updated successfully!")
        
        # Redirect the user to their profile page
        return redirect('userprofile')
    
    # Render the update profile form for GET requests
    return render(request, 'update.html')


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import CartItem
import json

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        price = request.POST.get('price')
        
        # Check if the item already exists in the user's cart
        existing_item = CartItem.objects.filter(user=request.user, item_name=item_name).first()
        if existing_item:
            existing_item.quantity += 1
            existing_item.save()
        else:
            CartItem.objects.create(user=request.user, item_name=item_name, price=price)

        return redirect('portfolio')
    else:
        return redirect('portfolio')

@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        item_id = json.loads(request.body).get('item_id')
        
        # Check if the item exists in the user's cart
        try:
            cart_item = CartItem.objects.get(user=request.user, id=item_id)
            cart_item.delete()

            # Calculate the total price
            total_price = calculate_total_price(request.user)

            return JsonResponse({'message': 'Item removed successfully', 'total_price': total_price}, status=200)

        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found in cart'}, status=404)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def update_cart(request):
    if request.method == 'POST':
        try:
            updated_cart_data = json.loads(request.body)
            
            for item_data in updated_cart_data:
                item_name = item_data.get('item_name')  # Changed to item_name
                quantity = item_data.get('quantity')
                
                if quantity == 0 or quantity > 9:  # Delete item if quantity is 0 or greater than 9
                    CartItem.objects.filter(user=request.user, item_name=item_name).delete()  # Changed to item_name
                else:
                    cart_item = CartItem.objects.get(user=request.user, item_name=item_name)  # Changed to item_name
                    cart_item.quantity = quantity
                    cart_item.save()
            
            total_price = calculate_total_price(request.user)
            
            return JsonResponse({'message': 'Changes saved successfully', 'total_price': total_price}, status=200)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def calculate_total_price(user):
    cart_items = CartItem.objects.filter(user=user)
    total_price = sum(item.price * item.quantity for item in cart_items)
    return total_price
    
from django.shortcuts import render
from .models import CartItem

@login_required
def cart(request):
  # Retrieve cart items and calculate total price
  cart_items = CartItem.objects.filter(user=request.user)
  calculated_total_price = calculate_total_price(user=request.user)  # Assuming calculate_total_price function exists

  # Add calculated_total_price to context dictionary
  context = {'cart_items': cart_items, 'calculated_total_price': calculated_total_price}

  # Print total price for verification (optional)
  print(calculated_total_price)  # Add this line

  return render(request, 'cart.html', context)

from django.http import JsonResponse
from .models import CartItem

@login_required
def delete_item(request):
    if request.method == 'POST':
        data = request.POST
        item_id = data.get('item_id')
        try:
            item = YourItemModel.objects.get(id=item_id)
            item.delete()
            return JsonResponse({'message': 'Item deleted successfully.'})
        except YourItemModel.DoesNotExist:
            return JsonResponse({'error': 'Item not found.'}, status=404)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

