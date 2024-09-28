# permissions.py
from rest_framework import permissions

class IsOwnerOrCollaborator(permissions.BasePermission):
    """
    Custom permission to only allow owners or collaborators of a Work Board to access it.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the Work Board or has a collaborator role
        user_role = obj.user_roles.filter(user=request.user).first()
        return user_role is not None and (user_role.role == 'Owner' or user_role.role == 'Collaborator')
