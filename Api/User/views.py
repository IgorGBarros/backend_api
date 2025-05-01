from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import CustomTokenObtainPairSerializer, CustomUserSerializer
from .models import CustomUser
from rest_framework import generics 
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.contrib.auth import get_user_model

# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]  # Permissão para qualquer usuário


User = get_user_model()


class FirebaseLoginView(APIView):
    def post(self, request, *args, **kwargs):
        firebase_token = request.data.get("firebase_token")
        
        if not firebase_token:
            return Response({"error": "Token do Firebase é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Cria ou obtém o usuário usando o token do Firebase
            user = User.objects.create_user_with_firebase(firebase_token)
            print(f"Usuário autenticado com sucesso: {user.email}")  # Log da mensagem no console do Docker

            return Response({"message": "Usuário autenticado com sucesso.", "email": user.email})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


