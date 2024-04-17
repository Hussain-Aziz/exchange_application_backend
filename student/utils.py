from knox.auth import AuthToken

def get_user_from_token(request):
    token = request.headers.get('Authorization').split(' ')[1]

    user = AuthToken.objects.filter(token_key__startswith=token[:8]).first().user # type: ignore
    return user