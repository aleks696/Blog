from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm, CustomUserCreationForm
from .models import Profile, User, FriendRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}.')
                return redirect('posts')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    # Check if session time is up
    if 'AUTO_LOGOUT_MESSAGE' in request.session:
        messages.info(request, request.session.pop('AUTO_LOGOUT_MESSAGE'))

    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'blog.html',
                  {})
def authView(request):
    """ Registration """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html',
                  {'form':form})

@login_required
@require_http_methods(["POST"])
def delete_account(request):
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, "Your account has been deleted.")
    return redirect('posts')


@login_required
def logout_view(request):
    logout(request)
    return redirect('posts')


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    incoming_requests = FriendRequest.objects.filter(receiver=request.user, is_active=True)
    outgoing_requests = FriendRequest.objects.filter(sender=request.user, is_active=True)

    friends = profile.friends.all()
    is_friend = profile.friends.filter(id=request.user.id).exists()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests,
        'is_friend': is_friend,
    }

    return render(request, 'profile.html', context)

@login_required
def author_profile_view(request, username):
    author = get_object_or_404(User, username=username)
    profile = author.profile
    is_friend = profile.friends.filter(id=request.user.profile.id).exists()
    incoming_requests = FriendRequest.objects.filter(receiver=request.user, is_active=True)
    outgoing_requests = FriendRequest.objects.filter(sender=request.user, is_active=True)

    context = {
        'profile': profile,
        'is_friend': is_friend,
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests,
    }
    return render(request, 'author_profile.html', context)
@login_required
@require_http_methods(["POST"])
def delete_user(request, username):
    user = get_object_or_404(User, username=username)
    if request.user.username:
        user.delete()
        return redirect('posts')

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': 'localhost:8000', # Change to your domain
                        'site_name': 'MyBlog',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset_form.html", context={"password_reset_form":password_reset_form})

@login_required
def send_friend_request(request, username):
    receiver = get_object_or_404(User, username=username)
    friend_request, created = FriendRequest.objects.get_or_create(sender=request.user, receiver=receiver)
    return redirect('author_profile', username=receiver.username)

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.receiver == request.user:
        friend_request.accept()
    return redirect('profile')

@login_required
def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.receiver == request.user:
        friend_request.decline()
    return redirect('profile')

@login_required
def cancel_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.sender == request.user:
        friend_request.cancel()
    return redirect('profile')

@login_required
def remove_friend(request, username):
    friend = get_object_or_404(User, username=username)
    request.user.profile.friends.remove(friend.profile)
    return redirect('profile')
