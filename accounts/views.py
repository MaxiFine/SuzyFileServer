from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages

from .forms import SignUpForm, LoginForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            # Email user for account verification
            host_name = request.get_host()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = f"{request.scheme}://{host_name}{reverse('activate', kwargs={'uidb64': uid, 'token': token})}"
            email_html_message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'activation_link':activation_link,
            })
            
            email = EmailMessage(
                'Account Activation',
                email_html_message,
                from_email='Suzzy',
                to=[user.email],
            )
            
            email.content_subtype="html"
            email.send()
            messages.info(request=request, message='Your account have been created. '
                          'A link has been sent to your Email address, '
                           'click on the link to activate your account to login')
            print(user.email)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request=request, message='Congratulations! You have activated your account. '
                         'Kindly Login to access the files')
        return redirect('login')
    else:
        messages.error(request, 'Invalid Activation Link, the link last for only 24hrs. '
                       'kindly signup again for a new link and activate as soon as possible. ')
        return redirect('login')
    
def login_view(request):
    # direct authenticated users to home 
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('feed')
                messages.warning(request, 'Account Not Activated. Check Your Email/Spam for Activation link! to verify your account.')
                return redirect('login')
            messages.error(request, 'Wrong Email or Password! Please check your details properly. ')
            return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

    
    