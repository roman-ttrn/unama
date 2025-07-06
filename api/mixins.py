from rest_framework import permissions

from .permissions import IsStaffEditorPermission

class IsStaffEditorMixin():
    permission_classes = [permissions.IsAdminUser,
                          IsStaffEditorPermission]

class FilterUserProducts():
    user_field = 'user'
    def get_queryset(self, *args, **kargs):
        lookup_data = {self.user_field: self.request.user}
        qs = super().get_queryset(*args, **kargs)
        if self.request.user.is_staff:
            return qs
        print(super())
        return qs.filter(**lookup_data)