"""
Role-based access control decorators for AgriScan+ system.

Usage:
    @role_required(['farmer', 'technician', 'admin'])
    def some_view(request):
        # Only accessible by specified roles
        pass
        
    @admin_only
    def admin_view(request):
        # Only admins can access
        pass
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


def role_required(allowed_roles):
    """
    Decorator to restrict access to views based on user role.
    
    Args:
        allowed_roles: List of allowed role strings ['farmer', 'technician', 'admin']
        
    Example:
        @role_required(['technician', 'admin'])
        def validate_detection(request, pk):
            # Only technicians and admins can access
            pass
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Check if user is authenticated
            if not request.user.is_authenticated:
                messages.error(request, "Please login to access this page.")
                return redirect('polls:login')
            
            # Get user profile and role
            profile = getattr(request.user, 'profile', None)
            
            if not profile:
                messages.error(request, "User profile not found. Please contact administrator.")
                return redirect('polls:dashboard')
            
            # Check if user's role is in allowed roles
            if profile.role not in allowed_roles:
                messages.error(
                    request, 
                    f"Access denied. This page is only accessible to: {', '.join(allowed_roles)}."
                )
                return redirect('polls:dashboard')
            
            # User has required role, proceed to view
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def admin_only(view_func):
    """
    Decorator to restrict access to admins only.
    
    Example:
        @admin_only
        def manage_users(request):
            # Only admins can access
            pass
    """
    return role_required(['admin'])(view_func)


def technician_or_admin(view_func):
    """
    Decorator to restrict access to technicians and admins.
    
    Example:
        @technician_or_admin
        def validate_detection(request, pk):
            # Technicians and admins can validate
            pass
    """
    return role_required(['technician', 'admin'])(view_func)


def farmer_only(view_func):
    """
    Decorator to restrict access to farmers only.
    Rarely used, but available for farmer-specific features.
    """
    return role_required(['farmer'])(view_func)


def get_user_role(request):
    """
    Helper function to get the current user's role.
    
    Returns:
        str: Role name ('farmer', 'technician', 'admin') or None
    """
    if not request.user.is_authenticated:
        return None
    
    profile = getattr(request.user, 'profile', None)
    return profile.role if profile else None


def is_admin(request):
    """Check if current user is admin."""
    return get_user_role(request) == 'admin'


def is_technician(request):
    """Check if current user is technician."""
    return get_user_role(request) == 'technician'


def is_farmer(request):
    """Check if current user is farmer."""
    return get_user_role(request) == 'farmer'


def can_edit_detection(request, detection):
    """
    Check if user can edit a specific detection record.

    Rules:
        - Admins: Can edit all
        - Technicians: Can validate/correct all
        - Farmers: Can edit only their own detections
    """
    role = get_user_role(request)

    if role in ('admin', 'technician'):
        return True

    if role == 'farmer':
        profile = getattr(request.user, 'profile', None)
        return profile is not None and detection.user == profile

    return False


def can_delete_detection(request, detection):
    """
    Check if user can delete a specific detection record.

    Rules:
        - Admins: Can delete all
        - Technicians: Can delete all (for data moderation)
        - Farmers: Can delete only their own detections
    """
    role = get_user_role(request)

    if role in ('admin', 'technician'):
        return True

    if role == 'farmer':
        profile = getattr(request.user, 'profile', None)
        return profile is not None and detection.user == profile

    return False


def filter_queryset_by_role(request, queryset, user_field='user'):
    """
    Filter queryset based on user role.
    
    Args:
        request: Django request object
        queryset: Django queryset to filter
        user_field: Name of the user/profile field (default: 'user')
        
    Returns:
        Filtered queryset based on role
        
    Example:
        detections = DetectionRecord.objects.all()
        detections = filter_queryset_by_role(request, detections, 'user')
    """
    role = get_user_role(request)
    
    if role == 'admin' or role == 'technician':
        # Admins and technicians see all
        return queryset
    
    if role == 'farmer':
        # Farmers only see their own data
        profile = getattr(request.user, 'profile', None)
        if profile:
            filter_kwargs = {user_field: profile}
            return queryset.filter(**filter_kwargs)
    
    # Default: return empty queryset if no role
    return queryset.none()
