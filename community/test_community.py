from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment, PostCategory
from django.utils import timezone
from .forms import CommentForm


class MusclePosts_test(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('muscle_posts')
        self.category_muscle = PostCategory.objects.create(name='Gain Muscle')
        self.post1 = Post.objects.create(title='Post 1', content='This is post 1', post_category=self.category_muscle)
        self.post2 = Post.objects.create(title='Post 2', content='This is post 2', post_category=self.category_muscle)

    def get_muscle_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post2.title)


class WeightPosts_test(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('weight_posts')
        self.category_weight = PostCategory.objects.create(name='Lose Weight')
        self.post1 = Post.objects.create(title='Post 1', content='This is post 1', post_category=self.category_weight)
        self.post2 = Post.objects.create(title='Post 2', content='This is post 2', post_category=self.category_weight)

    def get_weight_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post2.title)


class CreatePost_test(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.post_data = {
            'title': 'Test Post',
            'content': 'This is a test post.',
            'post_category': '1'
        }

    def reate_post(self):
        url = reverse('create_post')
        response = self.client.post(url, data=self.post_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)

        post = Post.objects.first()
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test post.')
        self.assertEqual(post.post_category.name, 'Gain Muscle')


class EditPost_test(TestCase):
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

    def edit_post(self):
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


class DeletePost_test(TestCase):
    def setUp(self):
        self.category = PostCategory.objects.create(name='Test Category')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            post_category=self.category,
        )
        self.url = reverse('delete_post', args=[self.post.id])

    def delete_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))


class EditComment_test(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass'
        )
        self.post = Post.objects.create(
            title='Test Post', 
            content='This is a test post.',
            name=self.user.username
        )
        self.comment = Comment.objects.create(
            post=self.post,
            name=self.user.username,
            content='This is a test comment.'
        )
        self.url = reverse('edit_comment', kwargs={'comment_id': self.comment.id})
        self.client.login(username='testuser', password='testpass')

    def edit_comment(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/comment_edit.html')


class DeleteComment_test(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='Test Post', content='Test Content')
        self.comment = Comment.objects.create(post=self.post, name='Test User', body='Test Comment Body')

    def delete_comment(self):
        response = self.client.get(reverse('delete_comment', args=[self.comment.id]))
        self.assertRedirects(response, reverse('post_detail', args=[self.post.id]))
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())


if __name__ == '__main__':
    unittest.main()



