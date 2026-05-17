from rest_framework.permissions import BasePermission

class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        return obj.author_id == request.user.id
