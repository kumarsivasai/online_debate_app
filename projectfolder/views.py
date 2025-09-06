from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from demoapp.models import RegisterUsers, LoginUsers


# ---- Test Views ----
def hello(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def kumar(request):
    return HttpResponse("hello everyone this is kumar")


# ---- Register ----
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        role = request.POST.get("role")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Password match check
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Check duplicates
        if RegisterUsers.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if RegisterUsers.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        # Save user in RegisterUsers
        user = RegisterUsers(
            username=username,
            email=email,
            phone=phone,
            role=role,
            password=make_password(password1)
        )
        user.save()

        # Also save user in LoginUsers
        login_user = LoginUsers(
            username=username,
            password=make_password(password1)
        )
        login_user.save()

        messages.success(request, "Registered successfully! Please login.")
        return redirect("login")

    return render(request, "login_system/register.html")


# ---- Login ----
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = RegisterUsers.objects.get(username=username)
        except RegisterUsers.DoesNotExist:
            messages.error(request, "Invalid username.")
            return redirect("login")

        if check_password(password, user.password):
            # Clear old session and set new
            request.session.flush()
            request.session["username"] = user.username
            request.session["role"] = user.role

            messages.success(request, f"Welcome {user.username}!")

            if user.role == "producer":
                return redirect("producer_home")
            else:
                return redirect("customer_home")
        else:
            messages.error(request, "Invalid password.")
            return redirect("login")

    return render(request, "login_system/login.html")


# ---- Customer Home ----
def customer_home(request):
    username = request.session.get("username", "")
    if not username:
        return redirect("login")
    return render(request, "customer_pages/customer_home.html", {"username": username})


# ---- Producer Home ----
def producer_home(request):
    username = request.session.get("username", "")
    if not username:
        return redirect("login")
    return render(request, "producer_pages/producer_home.html", {"username": username})


# ---- Logout ----
def logout_view(request):
    request.session.flush()   # clears all session data
    logout(request)
    return redirect("login")
