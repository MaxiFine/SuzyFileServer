# # CBV imports
# from django.contrib.auth.forms import UserCreationForm
# from django.urls import reverse_lazy
# from django.views.generic import CreateView


# FBV imports
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .forms import SignUpForm



# # Class Based View to test the signup
# class SignUpView(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"



# FBV for user signups
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            return redirect('login')  # Redirect to the login page
    else:
        form = SignUpForm()
        # Restrict the UserCreationForm fields to only email and password
        # form.fields.pop('username')
    return render(request, 'registration/signup.html', {'form': form})



    