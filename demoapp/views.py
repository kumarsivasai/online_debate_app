from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from demoapp.models import RegisterUsers, LoginUsers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


#--------------------------------------------------register view--------------------------------------------------#

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if RegisterUsers.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if RegisterUsers.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        user = RegisterUsers(
            username=username,
            email=email,
            phone=phone,
            password=make_password(password1)
        )
        user.save()

        login_user = LoginUsers(username=username, password=make_password(password1))
        login_user.save()

        messages.success(request, "Registered successfully! Please login.")
        return redirect("login")

    return render(request, "login_system/register.html")


#--------------------------------------------------API Register View--------------------------------------------------#

from .models import RegisterUsers, LoginUsers  # Import your login model

@csrf_exempt
def api_register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            username = data.get("username")
            email = data.get("email")
            phone = data.get("phone")
            password1 = data.get("password1")
            password2 = data.get("password2")

            if password1 != password2:
                return JsonResponse({"error": "Passwords do not match"}, status=400)

            if RegisterUsers.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            if RegisterUsers.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already exists"}, status=400)

            # Save in RegisterUsers
            user = RegisterUsers(
                username=username,
                email=email,
                phone=phone,
                password=make_password(password1)
            )
            user.save()

            # Also save in LoginUsers
            login_user = LoginUsers(
                username=username,
                password=make_password(password1)
            )
            login_user.save()

            return JsonResponse({"message": "Registered successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=405)


#--------------------------------------------------login view--------------------------------------------------#

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
            # Clear old session and set new session data
            request.session.flush()
            request.session["username"] = user.username
            return redirect("home")   # ✅ redirect all users to one home page
        else:
            messages.error(request, "Invalid password.")
            return redirect("login")

    return render(request, "login_system/login.html")


#--------------------------------------------------API Login View--------------------------------------------------#


@csrf_exempt
def api_login(request):
    if request.method == "POST":
        try:
            # Parse JSON body
            data = json.loads(request.body.decode("utf-8"))
            username = data.get("username")
            password = data.get("password")

            # Check if user exists
            try:
                user = RegisterUsers.objects.get(username=username)
            except RegisterUsers.DoesNotExist:
                return JsonResponse({"error": "User does not exist"}, status=404)

            # Verify password
            if not check_password(password, user.password):
                return JsonResponse({"error": "Invalid password"}, status=400)

            # Success response
            return JsonResponse({
                "message": "Login successful",
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone
                }
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # Method not allowed
    return JsonResponse({"error": "Invalid method"}, status=405)



#--------------------------------------------------home & logout--------------------------------------------------#




def logout_view(request):
    request.session.flush()  # Clear session data
    logout(request)           # Django auth logout (optional)
    return redirect("login")  # Redirect to login page

def home_view(request):
    username = request.session.get("username", "")
    return render(request, "dashboard/home.html", {"username": username})
