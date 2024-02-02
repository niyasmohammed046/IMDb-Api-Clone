from rest_framework.decorators import api_view
from . serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

@api_view(['POST',])
def registation_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        detail = {}            

        if serializer.is_valid():
            ac = serializer.save()

            detail['username'] = ac.username
            detail['email'] = ac.email

            token = Token.objects.get(user=ac).key   
            detail['token'] = token
        else:
            detail = serializer.errors
        return Response(detail,status=status.HTTP_201_CREATED)
    
@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)