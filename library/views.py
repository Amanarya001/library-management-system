from django.http import HttpResponse
from library.models import CustomUser
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import Book, Category
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
User = get_user_model()



# Create your views here.
def index(request):
    return render(request, 'index.html', )

# Create your login here.
def login(request):  
    if request.method == 'POST':
        username =request.POST.get("username")
        password =request.POST.get("password")
     
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # log the user in
            return redirect("homepage2")  # redirect to your home page
        else:
            msg_data = " Invalid username or password"
            return render(request, 'library/homepage.html', {'msg_data': msg_data})
    return render(request,'library/login.html')

# Step 1: forgot_passward  page  
def forgot_pass(request):
    User = get_user_model()
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)   # ✅ check if email exists
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
        except User.DoesNotExist:
            msg = "Email not registered."
            return render(request, "library/forgot_pass.html", {"msg_data": msg})

        # ✅ If email exists → send reset link (basic example)
        reset_link = request.build_absolute_uri(
        reverse("reset_password", kwargs={"uidb64": uid, "token": token})
        )
        send_mail(
            subject="Password Reset Request",
            message=f"Hi {user.username},\n\nClick below to reset your password:\n{reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        msg ="✅ Password reset link sent to your email."
        return render(request, "library/forgot_pass.html", {"msg_data": msg})

    return render(request, "library/forgot_pass.html")

# Step 2: Reset Password - set new password
def reset_password(request, uidb64, token):
    msg_data = ""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            p1 = request.POST.get("password1")
            p2 = request.POST.get("password2")
            if p1 == p2:
                user.password = make_password(p1)
                user.save()
                msg_data = "✅ Password successfully reset. You can login now."
                return redirect("homepage")  # redirect to your login page
            else:
                msg_data = "❌ Passwords do not match."
        return render(request, "library/reset_password.html", {"msg_data": msg_data})
    else:
        msg_data = "❌ Invalid or expired link."
        return render(request, "library/reset_password.html", {"msg_data": msg_data })

#User creation page
def register(request):
    msg_data = ""
    if  request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        location = request.POST.get('location')
        bio = request.POST.get('bio')

        # ✅ check if user already exists
        if CustomUser.objects.filter(username=username).exists():
            msg_data = "❌This username already exists"
            return render(request, "library/register.html", {'msg_data': msg_data})
        
        if CustomUser.objects.filter(phone=phone).exists():
            msg_data = "❌This phone Number already exists"
            return render(request, "library/register.html", {'msg_data': msg_data})
        
        elif CustomUser.objects.filter(email=email).exists():
            msg_data = "❌This email is already registered"
            return render(request, "library/register.html", {'msg_data': msg_data})

        else:
            if password == confirm_password:
                # ✅ create new user
                user_obj = CustomUser.objects.create_user(
                    username=username,
                    phone=phone,
                    email=email,
                    password=password,
                    location=location,
                    bio=bio
                )
                return redirect('homepage')
            else:
                msg_data = "❌Password and Confirm Password do not match"
                return render(request, "library/register.html", {'msg_data': msg_data})

    return render(request, "library/register.html")

# Create your homepage here.
def homepage(request):
    return render(request, "library/homepage.html")

# Create your homepage after login here.
def homepage2(request):
    return render(request, "library/homepage2.html")

# Create your add_book here.
def add_book(request):
    categories = Category.objects.all()  # send categories to template

    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        category = request.POST.get("category")
        published_date = request.POST.get("published_date")

        Book.objects.create(
            title=title,
            author=author,
            category=category,
            published_date=published_date if published_date else None
        )

        return redirect("book_list")  # redirect to list of books

    return render(request, "library/add_book.html", {"categories": categories})

# Create your book_list here.
def book_list(request):
    books = Book.objects.all()  # Fetch all added books
    return render(request, 'library/book_list.html', {'books': books})

# Create your about us here.
def about_us(request):
    return render(request, 'library/about_us.html')

# Create your book_list here.
def contact_us(request):
    return render(request, 'library/contact_us.html')
    
# change_passward - set new password
@login_required
def change_password(request):
    msg_data = ""

    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")   
        new_password2 = request.POST.get("new_password2")


        user = request.user

        # Check old password
        if not user.check_password(old_password):
            msg_data = "❌ Old password is incorrect."
            

        # Check new passwords match
        elif new_password1 != new_password2:
            msg_data = "❌New Password and Confirm New Password do not match"

        else:
            # Set new password and keep user logged in
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)
            msg_data = "✅ Password successfully changed."

    return render(request, "library/change_password.html", {'msg_data': msg_data})


# Create your edit_profile page
@login_required
def edit_profile(request):
    user = request.user  # CustomUser instance
    msg_data = ""

    if request.method == "POST":
        username = request.POST.get("username")  # if you allow editing username
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        fullName = request.POST.get("fullName")
        location = request.POST.get("location")
        bio = request.POST.get("bio")

        # --- Validation ---
        if username and CustomUser.objects.exclude(pk=user.pk).filter(username=username).exists():
            msg_data = "❌This username already exists"
        elif phone and CustomUser.objects.exclude(pk=user.pk).filter(phone=phone).exists():
            msg_data = "❌This phone number already exists"
        elif email and CustomUser.objects.exclude(pk=user.pk).filter(email=email).exists():
            msg_data = "❌This email is already registered"
        else:
            # --- Save updates ---
            user.username = username
            user.email = email
            user.phone = phone
            user.location = location
            user.bio = bio

            if "avatar" in request.FILES:
                user.avatar = request.FILES["avatar"]

            user.save()
            msg_data = "✅Profile updated successfully"

    return render(request, "library/edit_profile.html", {"user": user, "msg_data": msg_data})

# redirect to homepage after logout
def logout_view(request):
    logout(request)
    return redirect('homepage')



 


