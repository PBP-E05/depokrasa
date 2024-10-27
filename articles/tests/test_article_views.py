from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from articles.models import Article, Comment, Category

class ArticleViewsTest(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create a category
        self.category = Category.objects.create(name='test_category')

        # Create an article
        self.article = Article.objects.create(
            title='Test Article',
            body='This is a test article.'
        )

        # Add a category for test article
        self.article.categories.add(self.category) 

    def test_show_articles(self):
        response = self.client.get(reverse('articles:show_articles')) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_show_article_category(self):
        response = self.client.get(reverse('articles:show_article_category', kwargs={'category': self.category.name}))         
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')

    def test_article_content(self):
        response = self.client.get(f'/articles/{self.article.pk}/') 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)

    def test_show_articles_json(self):
        response = self.client.get(reverse('articles:show_articles_json')) 
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [self.article.to_dict()]) 
    
    def test_show_articles_by_category_json(self):
        response = self.client.get(reverse('articles:show_articles_by_category_json', kwargs={'category': self.category.name})) 
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [article.to_dict() for article in Article.objects.filter(categories__name__contains= self.category).order_by("-created_on")]) 

    def test_add_comment_ajax(self):
        self.client.login(username='testuser', password='testpass')  # Log in the user
        response = self.client.post(reverse('articles:add_comment_ajax'), {
            'comment': 'This is a test comment.',
            'article_id': self.article.pk
        })  

        comment_data = Comment.objects.get(author=self.user, article=self.article, body='This is a test comment.')
        
        # Test the to_dict method
        expected_dict = {
            'id': comment_data.id,
            'body': comment_data.body,
            'created_on': comment_data.created_on.isoformat(),
            'author': {
                'username': comment_data.author.username,
                'profile_picture': comment_data.author.profile_picture.url if hasattr(comment_data.author, 'profile_picture') else '/media/profile_pictures/default.jpg'
            },
            'article_id': comment_data.article.id,
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(comment_data.to_dict(), expected_dict)

         # Test adding empty comment
        get_empty_comment_body_response = self.client.post(reverse('articles:add_comment_ajax'), {
            'comment': '',
            'article_id': self.article.pk
        })  
        self.assertEqual(get_empty_comment_body_response.status_code, 400)
        self.assertEqual(get_empty_comment_body_response.json(), {"error": "BAD REQUEST: empty comment"})

    def test_show_comments_json(self):
        # First, add a comment to test the JSON response
        self.client.login(username='testuser', password='testpass')  # Log in the user

        get_not_article_id_response = self.client.get(reverse('articles:show_comments_json')) 
        self.assertEqual(get_not_article_id_response.status_code, 200)
        comments_data = get_not_article_id_response.json()
        self.assertEqual(len(comments_data), 0)  
        self.assertEqual(comments_data, [])


        post_response = self.client.post(reverse('articles:add_comment_ajax'), {
            'comment': 'Another test comment.',
            'article_id': self.article.pk
        }) 

        get_comments_response = self.client.get(reverse('articles:show_comments_json'), {'article_id': self.article.pk}) 
        self.assertEqual(get_comments_response.status_code, 200)
        comments_data = get_comments_response.json()
        self.assertGreater(len(comments_data), 0)  
        self.assertEqual(comments_data[0]['body'], 'Another test comment.')

