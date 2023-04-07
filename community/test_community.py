from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment, PostCategory
from django.utils import timezone
from .forms import CommentForm



class MusclePostsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('muscle_posts')
        self.category_muscle = PostCategory.objects.create(name='Gain Muscle')
        self.post1 = Post.objects.create(title='Post 1', content='This is post 1', post_category=self.category_muscle)
        self.post2 = Post.objects.create(title='Post 2', content='This is post 2', post_category=self.category_muscle)

    def test_get_muscle_posts(self):
        """Test that muscle_posts view returns posts with Gain Muscle category"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post2.title)

    def test_context_data(self):
        """Test that the context contains the correct data"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts_muscle'], [repr(self.post1), repr(self.post2)])


class WeightPostsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('weight_posts')
        self.category_weight = PostCategory.objects.create(name='Lose Weight')
        self.post1 = Post.objects.create(title='Post 1', content='This is post 1', post_category=self.category_weight)
        self.post2 = Post.objects.create(title='Post 2', content='This is post 2', post_category=self.category_weight)

    def test_get_weight_posts(self):
        """Test that weight_posts view returns posts with Lose Weight category"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post2.title)

    def test_context_data(self):
        """Test that the context contains the correct data"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts_weight'], [repr(self.post1), repr(self.post2)])


class CheckPostIdTestCase(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='Post 1', content='This is post 1')
        self.comment1 = Comment.objects.create(post=self.post, content='This is a comment')
        self.comment2 = Comment.objects.create(post=self.post, content='This is another comment')

    def test_check_post_id_true(self):
        """Test that check_post_id returns True when the comment's post is the same as the given post"""
        result = check_post_id(self.post, self.comment1)
        self.assertEqual(result, True)

    def test_check_post_id_false(self):
        """Test that check_post_id returns False when the comment's post is not the same as the given post"""
        post2 = Post.objects.create(title='Post 2', content='This is post 2')
        comment3 = Comment.objects.create(post=post2, content='This is a comment on post 2')
        result = check_post_id(self.post, comment3)
        self.assertEqual(result, False)


class TestPostDetailCreateComment(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(title='Test Post', content='Test content')
        self.url = reverse('post_detail', args=[self.post.id])
        self.valid_data = {'name': 'Test Name', 'email': 'test@example.com', 'body': 'Test comment body'}

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/blog_details.html')
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)

    def test_post_valid_data(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        comment = Comment.objects.get(name=self.valid_data['name'])
        self.assertEqual(comment.body, self.valid_data['body'])
        self.assertEqual(comment.email, self.valid_data['email'])

    def test_post_invalid_data(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/blog_details.html')
        self.assertFormError(response, 'comment_form', 'name', 'This field is required.')
        self.assertFormError(response, 'comment_form', 'email', 'This field is required.')
        self.assertFormError(response, 'comment_form', 'body', 'This field is required.')


class CreatePostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.post_data = {
            'title': 'Test Post',
            'content': 'This is a test post.',
            'post_category': '1'
        }

    def test_create_post(self):
        url = reverse('create_post')
        response = self.client.post(url, data=self.post_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)

        post = Post.objects.first()
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test post.')
        self.assertEqual(post.post_category.name, 'Gain Muscle')


class EditPostTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.post = Post.objects.create(
            title='Test post',
            content='Test content',
            author=self.user,
            post_date=timezone.now()
        )
        self.edit_url = reverse('edit_post', args=[self.post.id])

    def test_get_edit_post_page(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/blogs_edit.html')
        self.assertIsInstance(response.context['post_form'], PostForm)
        self.assertEqual(response.context['post_form'].instance, self.post)

    def test_edit_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.edit_url, {
            'title': 'Updated test post',
            'content': 'Updated test content',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post_detail', args=[self.post.id]))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated test post')
        self.assertEqual(self.post.content, 'Updated test content')

    def test_invalid_edit_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.edit_url, {
            'title': '',
            'content': 'Updated test content',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/blogs_edit.html')
        self.assertIsInstance(response.context['post_form'], PostForm)
        self.assertEqual(response.context['post_form'].instance, self.post)
        self.assertContains(response, "This field is required.")


class DeletePostTestCase(TestCase):

    def setUp(self):
        self.category = PostCategory.objects.create(name='Test Category')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            post_category=self.category,
        )
        self.url = reverse('delete_post', args=[self.post.id])

    def test_delete_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_delete_post_weight(self):
        category_weight = PostCategory.objects.create(name='Lose Weight')
        post_weight = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            post_category=category_weight,
        )
        url = reverse('delete_post', args=[post_weight.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('weight_posts'))

    def test_delete_post_muscle(self):
        category_muscle = PostCategory.objects.create(name='Gain Muscle')
        post_muscle = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            post_category=category_muscle,
        )
        url = reverse('delete_post', args=[post_muscle.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('muscle_posts'))


class EditCommentTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass'
        )
        self.post = Post.objects.create(
            title='Test Post', 
            content='This is a test post.',
            email=self.user.email,
            name=self.user.username
        )
        self.comment = Comment.objects.create(
            post=self.post,
            name=self.user.username,
            email=self.user.email,
            content='This is a test comment.'
        )
        self.url = reverse('edit_comment', kwargs={'comment_id': self.comment.id})
        self.client.login(username='testuser', password='testpass')

    def test_edit_comment_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/comment_edit.html')

    def test_edit_comment_form_valid(self):
        data = {
            'content': 'This is an edited comment.'
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('post_detail', kwargs={'post_id': self.post.id}))
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'This is an edited comment.')

    def test_edit_comment_form_invalid(self):
        data = {
            'content': ''
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/comment_edit.html')
        self.assertIn('This field is required.', response.content.decode())


class TestDeleteComment(TestCase):

    def setUp(self):
        self.post = Post.objects.create(title='Test Post', content='Test Content')
        self.comment = Comment.objects.create(post=self.post, name='Test User', email='testuser@test.com', body='Test Comment Body')

    def test_delete_comment(self):
        response = self.client.get(reverse('delete_comment', args=[self.comment.id]))
        self.assertRedirects(response, reverse('post_detail', args=[self.post.id]))
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

