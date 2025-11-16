from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer

class UserRegistrationView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'tokens': {
                'refresh': str(token),
                'access': str(token.access_token)
            }
        }, status=status.HTTP_201_CREATED)

class UserLoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # login serializer returns {'user': user}
        user = serializer.validated_data.get('user')
        token = RefreshToken.for_user(user)
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'tokens': {
                'refresh': str(token),
                'access': str(token.access_token)
            }
        }, status=status.HTTP_200_OK)
