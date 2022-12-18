from django.shortcuts import redirect


def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated or request.session.get('is_authenticated'):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('front:login')

    return wrapper_func
