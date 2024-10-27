
from django.test import TestCase, Client
from django.contrib.auth.models import User
from ..models import Category, Article, Comment
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Test Category")

    def test_category_str_method(self):
        self.assertEqual(str(self.category), "Test Category")

    def test_category_natural_key(self):
        self.assertEqual(self.category.natural_key(), ("Test Category",))

class ArticleModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.article = Article.objects.create(
            title="Test Article",
            body="This is the body of the test article.",
        )
        self.article.categories.add(self.category)

    def test_article_creation(self):
        self.assertEqual(self.article.title, "Test Article")
        self.assertEqual(self.article.body, "This is the body of the test article.")
        self.assertIn(self.category, self.article.categories.all())

    def test_article_str_method(self):
        self.assertEqual(str(self.article), "Test Article")

    def test_article_to_dict_method(self):
        article_dict = self.article.to_dict()
        self.assertEqual(article_dict["title"], "Test Article")
        self.assertEqual(article_dict["body"], "This is the body of the test article.")
        self.assertIn("Test Category", article_dict["categories"])

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(name="Test Category")
        self.article = Article.objects.create(
            title="Test Article",
            body="This is the body of the test article.",
        )
        self.comment = Comment.objects.create(
            author=self.user,
            article=self.article,
            body="This is a test comment."
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.body, "This is a test comment.")
        self.assertEqual(self.comment.author.username, "testuser")
        self.assertEqual(self.comment.article, self.article)

    def test_comment_str_method(self):
        self.assertEqual(str(self.comment), "testuser on Test Article")

    def test_comment_get_author_data(self):
        author_data = self.comment.get_author_data()
        self.assertEqual(author_data["username"], "testuser")
        # Assuming no profile picture is set, check default profile picture path
        self.assertEqual(author_data["profile_picture"], "/media/profile_pictures/default.jpg")

    def test_comment_to_dict_method(self):
        comment_dict = self.comment.to_dict()
        self.assertEqual(comment_dict["body"], "This is a test comment.")
        self.assertEqual(comment_dict["author"]["username"], "testuser")
        self.assertEqual(comment_dict["article_id"], self.article.id)
