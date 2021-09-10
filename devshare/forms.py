from django import forms
from resource.models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'article_title',
            'article_link',
            'article_info',
            'article_tag'
        ]

    