from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import AccountCreationSerializer, AccountManagementSerializer


class AccountCreationView(CreateAPIView):
    """Vue de l'API de création de compte utilisateur"""

    serializer_class = AccountCreationSerializer
    permission_classes = [AllowAny]


class AccountManagementView(RetrieveUpdateDestroyAPIView):
    """Vue de l'API de gestion de compte utilisateur"""

    serializer_class = AccountManagementSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user)
