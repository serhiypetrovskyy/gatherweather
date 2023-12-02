from rest_framework.response import Response
from rest_framework.decorators import api_view

from users.serializers import RegisterSerializer


@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Successfully registered a new user'
            data['username'] = user.username
            data['email'] = user.email
        else:
            data = serializer.errors
        return Response(data)



