class PermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add the `perms` variable to the template context
        def add_perms_to_context():
            return {'perms': request.user.get_all_permissions()}

        response = self.get_response(request)
        return response