from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import *


# VUES PUBLIQUES

class PublicAccountCreateView(CreateAPIView):
    """Vue de l'API publique de création de compte utilisateur"""

    serializer_class = PublicAccountCreationSerializer


class PublicAccountLoginView(ObtainAuthToken):
    """Vue de l'API publique de connexion de compte utilisateur"""

    serializer_class = PublicAccountLoginSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# VUES PRIVÉES

class PrivateAccountManageView(RetrieveUpdateAPIView):
    """Vue de l'API privée de gestion de compte utilisateur"""

    serializer_class = PrivateAccountManagementSerializer

    def get_object(self):
        return self.request.user
