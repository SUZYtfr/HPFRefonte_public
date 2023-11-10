from rest_framework import permissions, generics, decorators
from reviews.views import AllReviewViewset
from .serializers import AccountCreationSerializer, AccountManagementSerializer


class AuthenticatedUserView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    """Vue du compte authentifié"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountManagementSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AccountCreationSerializer
        return super().get_serializer_class()

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user)


# TODO - ExternalProfileViewSet