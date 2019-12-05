from articles.models import ArticleModel
from rest_framework.serializers import HyperlinkedModelSerializer


class PostSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ArticleModel
        fields = ['title', 'subtitle', 'short_description', 'body', 'author', 'creation_date',
                  'tags', 'main_theme']
