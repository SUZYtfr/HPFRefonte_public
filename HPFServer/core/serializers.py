from rest_framework import serializers


class ListableModelSerializer(serializers.ModelSerializer):
    """
    Ce sérialiseur permet de préciser le sérialiseur alternatif à utiliser comme élément de liste pour le modèle.
    ex. UserSerializer.Meta.list_serializer_child_class = UserListSerializer
    cf: https://github.com/encode/django-rest-framework/blob/101aff6c43f6fa96174683e050988428143d1040/rest_framework/serializers.py#L130
    TODO - Un mixin serait plus approprié, mais il s'agit d'une classmethod qui n'est pas héritée par l'enfant
    """

    @classmethod
    def many_init(cls, *args, **kwargs):
        meta = getattr(cls, 'Meta', None)
        list_kwargs = {'child': getattr(meta, "list_serializer_child_class", cls)()}  # enfant initialisé dès ici
        list_serializer_class = getattr(meta, 'list_serializer_class', serializers.ListSerializer)
        return list_serializer_class(*args, **list_kwargs)


class CardSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    string = serializers.CharField(source="__str__", read_only=True)
