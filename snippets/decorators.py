from django.core.exceptions import PermissionDenied
# from .models import UserSession
import functools
from django.shortcuts import redirect
from django.contrib import messages

def user_is_entry_author(function):
    def wrap(request, *args, **kwargs):
        # entry = UserSession.objects.get(pk=kwargs['entry_id'])
        if request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def authentication_not_required(view_func, redirect_url="accounts:profile"):
    """
        this decorator ensures that a user is not logged in,
        if a user is logged in, the user will get redirected to 
        the url whose view name was passed to the redirect_url parameter
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request,*args, **kwargs)
        messages.info(request, "You need to be logged out")
        print("You need to be logged out")
        return redirect(redirect_url)
    return wrapper