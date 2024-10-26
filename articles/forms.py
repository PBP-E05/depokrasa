from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from models import Article


class ArticleForm(forms.ModelForm):
      """Form for Article"""

      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["body"].required = False

      class Meta:
          model = Article
          fields = ("title","featured image", "body", "categories")
          widgets = {
              "text": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="article"
              )
          }