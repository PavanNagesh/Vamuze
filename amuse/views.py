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
    MAX_FAILED_ATTEMPTS = 3
    TIMEOUT_DURATION = timedelta(minutes=5)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check for session variables
        failed_attempts = request.session.get('failed_attempts', 0)
        lockout_time = request.session.get('lockout_time')

        # Check if the user is locked out
        if lockout_time:
            # Convert lockout_time to a datetime object
            lockout_time = datetime.fromisoformat(lockout_time)
            if datetime.now() < lockout_time:
                # User is still in lockout period
                messages.error(request, 'You have made too many failed login attempts. Please try again later.')
                return render(request, 'login.html')

            # Reset failed attempts and lockout time if the lockout period has passed
            request.session.pop('failed_attempts', None)
            request.session.pop('lockout_time', None)

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Successful login
            auth_login(request, user)
            # Reset failed attempts after successful login
            request.session.pop('failed_attempts', None)
            return redirect('index')
        else:
            # Increment failed attempts
            failed_attempts += 1
            request.session['failed_attempts'] = failed_attempts

            # Check if the user has reached the maximum failed attempts
            if failed_attempts >= MAX_FAILED_ATTEMPTS:
                # Calculate the lockout end time
                lockout_end_time = datetime.now() + TIMEOUT_DURATION
                # Store the lockout end time in the session
                request.session['lockout_time'] = lockout_end_time.isoformat()

                # Display an error message and return to the login page
                messages.error(request, 'You have made too many failed login attempts. Please try again later.')
                return render(request, 'login.html')

            # If failed attempts is less than the limit, display an error message
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

    # Handle GET requests
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
