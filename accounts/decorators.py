from django.http import HttpResponse
from django.shortcuts import redirect

# user is logged in or not
def unauthenticatedUser(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


# which user is allowed to visit which page
def allowedUsers(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                print('value of group: ',group)

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to visit this page')

        return wrapper_func
    return decorator


# this will help to redirect to admin and others categories to their associate root page
def adminOnly(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'admin':
                return view_func(request, *args, **kwargs)
            if group == 'customer':
                return redirect('user_profile')
    return wrapper_func
