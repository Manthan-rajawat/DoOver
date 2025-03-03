from .serializers import CreateUserSerializer, LoginSerializer,UserSerialiser,ChangePasswordSerializer
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.
# class UserListCreateApiView (generics.ListCreateAPIView):
#     queryset = CustomUser.objects.all()

#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return CreateUserSerializer
#         return UserSerialiser
    
# class UserDetailView (generics.RetrieveUpdateDestroyAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerialiser
#     permission_classes = [IsAuthenticated]

def get_tokens_for_user(user):
     refresh = RefreshToken.for_user(user)
     return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
     }

class UserApiView (APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserSerialiser(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateUserApiView (APIView):
    permission_classes = [AllowAny]
    
    def post(self,request,format=None):
        serializer = CreateUserSerializer(data = request.data)
        print(serializer)
        if  serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({"token":token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
    
class LoginView(APIView):
    permission_classes=[AllowAny]

    def post(self,request,format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=serializer.validated_data['username'],password=serializer.validated_data['password'])
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({"token":token}, status=status.HTTP_200_OK)
            else:
                return Response({"error":"Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView (APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = ChangePasswordSerializer(instance=request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg":"Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

