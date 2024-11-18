from django.shortcuts import redirect
from functools import wraps

def admin_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'admin_user_id' not in request.session:
            return redirect('login_admin')  # Redirect to the login page if not logged in
        return view_func(request, *args, **kwargs)
    return _wrapped_view
