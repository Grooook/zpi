
def generate_request_headers(request):
    if 'auth_token' in request.session:
        return {'Authorization': 'Token ' + request.session['auth_token']}
    return {}
