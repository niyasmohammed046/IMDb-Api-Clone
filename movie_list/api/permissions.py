from rest_framework import permissions

class AdminOrReadOnly(permissions.IsAdminUser): # this class is for admin can only edit others can read only

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)
        
    
class ReviewUserOrReadOnly(permissions.BasePermission): # this is for the review can edit only who created it and others can read it

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # safe_method means GET, that means they can see this
            return True
        else:                                           # this part means they are try to post,put or delete this part will work
           return obj.review_user == request.user