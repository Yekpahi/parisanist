from django.shortcuts import render, redirect
from userauths.forms import RegistrationForm
from django.contrib import messages, auth

from userauths.models import Account
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request, "You are successfully registered!!")
            return redirect('register')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            
            return redirect('home')
        else :
            messages.success(request, "Invalid login credentials")
            return redirect('login')
    
    return render(request, 'user/login.html')

@login_required(login_url= 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect('login')

# def activation_sent_view(request):
#     return render(request, 'user/activation_sent.html')


# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     # checking if the user exists, if the token is valid.
#     if user is not None and account_activation_token.check_token(user, token):
#         # if valid set active true
#         user.is_active = True
#         # set signup_confirmation true
#         user.profile.signup_confirmation = True
#         user.save()
#         login(request, user)
#         return redirect('home')
#     else:
#         return render(request, 'activation_invalid.html')

# def signup_view(request):
#     if request.method  == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()
#             user.user.firstname = form.cleaned_data.get('firstname')
#             user.user.lastname = form.cleaned_data.get('lastname')
#             user.user.email = form.cleaned_data.get('email')
#             # user can't login until link confirmed
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             subject = 'Please Activate Your Account'
#             # load a template like get_template()
#             # and calls its render() method immediately.
#             message = render_to_string('activation_request.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 # method will generate a hash value with user related data
#                 'token': account_activation_token.make_token(user),
#             })
#             user.email_user(subject, message)
#             return redirect('user/activation_sent')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'user/signup.html', {'form': form})


# def register_view(request):
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST or None)
#         if form.is_valid():
#             new_user = form.save()
#             firstname = form.cleaned_data.get("firstname")
#             messages.success(
#                 request, f"Hey {firstname}", "You account was was created successfully!")
#             new_user = authenticate(firstname=form.cleaned_data['email'],
#                                     password=form.cleaned_data['password1']
#                                     )
#             login(request, new_user)
#             return redirect("base:home")
#     else:
#         form = UserRegisterForm()

#     context = {
#         'form': form
#     }
#     return render(request, "user/signup.html", context)
