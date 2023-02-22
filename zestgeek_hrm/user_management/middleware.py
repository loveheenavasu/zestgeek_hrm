from django.shortcuts import redirect

class PermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in ['/department','/admin', '/roles', '/employee']:  # Add the URLs that you want to restrict access to here
            if not request.user.is_admin:
                print(request.user)
                return redirect('restricted')  # replace 'restricted' with the URL of the page you want to redirect to

        response = self.get_response(request)

        return response
