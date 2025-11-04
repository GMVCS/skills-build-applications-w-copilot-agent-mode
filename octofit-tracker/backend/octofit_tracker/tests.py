from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Team, Activity, Workout, LeaderboardEntry

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)

class TeamTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='teamuser', password='testpass')
        self.team = Team.objects.create(name='Test Team')
        self.team.members.add(self.user)

    def test_team_creation(self):
        self.assertEqual(Team.objects.count(), 1)
        self.assertIn(self.user, self.team.members.all())

class ActivityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='activityuser', password='testpass')
        self.activity = Activity.objects.create(user=self.user, activity_type='Run', duration=30, calories_burned=300, date='2025-11-04')

    def test_activity_creation(self):
        self.assertEqual(Activity.objects.count(), 1)

class WorkoutTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.workout = Workout.objects.create(name='Cardio', description='Cardio workout')

    def test_workout_creation(self):
        self.assertEqual(Workout.objects.count(), 1)

class LeaderboardEntryTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='leaderuser', password='testpass')
        self.team = Team.objects.create(name='Leaderboard Team')
        self.entry = LeaderboardEntry.objects.create(user=self.user, team=self.team, total_points=100)

    def test_leaderboard_entry_creation(self):
        self.assertEqual(LeaderboardEntry.objects.count(), 1)
