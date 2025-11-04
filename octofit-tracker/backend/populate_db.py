import os
import django
import random
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')
django.setup()

from octofit_tracker.models import User, Team, Activity, Workout, LeaderboardEntry

def create_users():
    users = []
    for i in range(5):
        user, created = User.objects.get_or_create(username=f'user{i+1}', defaults={
            'email': f'user{i+1}@example.com',
            'first_name': f'User{i+1}',
            'last_name': 'Test',
        })
        user.set_password('password')
        user.save()
        users.append(user)
    return users

def create_teams(users):
    teams = []
    for i in range(2):
        team, created = Team.objects.get_or_create(name=f'Team {i+1}')
        team.members.set(users[i*2:(i+1)*2+1])
        team.save()
        teams.append(team)
    return teams

def create_workouts(users):
    workouts = []
    for i in range(3):
        workout, created = Workout.objects.get_or_create(
            name=f'Workout {i+1}',
            defaults={'description': f'Description for workout {i+1}'}
        )
        workout.suggested_for.set(users[:2])
        workout.save()
        workouts.append(workout)
    return workouts

def create_activities(users):
    activities = []
    activity_types = ['Run', 'Bike', 'Swim']
    for user in users:
        for i in range(2):
            activity, created = Activity.objects.get_or_create(
                user=user,
                activity_type=random.choice(activity_types),
                duration=random.randint(20, 60),
                calories_burned=random.randint(200, 600),
                date=date.today() - timedelta(days=i)
            )
            activities.append(activity)
    return activities

def create_leaderboard_entries(users, teams):
    for user in users:
        LeaderboardEntry.objects.get_or_create(user=user, team=None, defaults={'total_points': random.randint(10, 100)})
    for team in teams:
        for user in team.members.all():
            LeaderboardEntry.objects.get_or_create(user=user, team=team, defaults={'total_points': random.randint(10, 100)})

def main():
    users = create_users()
    teams = create_teams(users)
    workouts = create_workouts(users)
    activities = create_activities(users)
    create_leaderboard_entries(users, teams)
    print('Test data created successfully.')

if __name__ == '__main__':
    main()
