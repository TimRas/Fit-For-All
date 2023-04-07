from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Challenge


class WorkoutPlansViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(title='Workouts')
        self.challenge1 = Challenge.objects.create(
            title='Challenge 1', 
            description='This is challenge 1', 
            category=self.category
        )
        self.challenge2 = Challenge.objects.create(
            title='Challenge 2', 
            description='This is challenge 2', 
            category=self.category
        )

    def test_workout_plans_view(self):
        response = self.client.get(reverse('workout_plans'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plans/workout_plans.html')
        self.assertQuerysetEqual(response.context['challenges'], 
                                 [repr(self.challenge1), repr(self.challenge2)], 
                                 ordered=False)


from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Challenge

class WorkoutPlansViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(title='Workouts')
        self.challenge1 = Challenge.objects.create(
            title='Challenge 1', 
            description='This is challenge 1', 
            category=self.category
        )
        self.challenge2 = Challenge.objects.create(
            title='Challenge 2', 
            description='This is challenge 2', 
            category=self.category
        )

    def test_workout_plans_view(self):
        response = self.client.get(reverse('workout_plans'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plans/workout_plans.html')
        self.assertQuerysetEqual(response.context['challenges'], 
                                 [repr(self.challenge1), repr(self.challenge2)], 
                                 ordered=False)
                                 

class TestViewChallenge(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(title="Workouts")
        self.challenge = Challenge.objects.create(title="30 Day Abs Challenge", description="Get those abs!", category=self.category)

    def test_view_challenge(self):
        url = reverse('view_challenge', args=[self.challenge.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plans/plans_details.html')
        self.assertContains(response, self.challenge.title)
        self.assertContains(response, self.challenge.description)
        self.assertEqual(response.context['challenge'], self.challenge)

