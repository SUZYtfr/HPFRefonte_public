from users.models import User, UserProfile
from graphene import ObjectType, Field, List, Int, Node
from graphene_django import DjangoObjectType


class ProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = [
            "realname",
            "bio",
        ]


class StatsType(ObjectType):
    fiction_count = Int()
    chapter_count = Int()
    word_count = Int()
    collection_count = Int()
    challenges = Int()
    review_count = Int()
    favorites_fanfictions = Int()
    favorites_series = Int()
    favorites_author = Int()


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]
        interfaces = [Node]


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            # "status",
            "first_seen",
        ]

    profile = Field(ProfileType)
    stats = Field(StatsType)
    
    @classmethod
    def resolve_stats(root, instance: User, info):
        return dict(
            fiction_count=instance.fiction_count,
            chapter_count=instance.chapter_count,
            word_count=instance.word_count,
            collection_count=instance.collection_count,
            challenges=0,
            review_count=0,
            favorites_fanfictions=0,
            favorites_series=0,
            favorites_author=0,
        )

    @classmethod
    def resolve_profile(root, instance: User, info):
        return instance.profile
