from django.db.transaction import atomic
from graphene import Mutation, Field, Int, String
from news.types import CommentType
from news.models import NewsComment


class PostComment(Mutation):
    class Arguments:
        news_id = Int(required=True)
        content = String(required=True)
    
    comment = Field(CommentType)

    @atomic
    def mutate(parent, info, news_id: int, content: str):
        from users.models import User
        user = User.objects.order_by("?").first()
        # user = info.context.user
        comment = NewsComment.objects.create(
            newsarticle_id=news_id,
            creation_user=user,
            text=content,
        )
        return PostComment(comment=comment)
