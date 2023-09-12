import pymongo
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    
    return render(request,  'index.html')

def create_user(request):
    """
    Create a new user.
    """
    username = request.POST['username']
    password = request.POST['password']

    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['TempUser']

    # Create a new user document.
    user = {
        'username': username,
        'password': password,
    }

    db.users.insert_one(user)

    return HttpResponse('User created successfully!')


def get_users(request):
    """
    Get all users.
    """
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['TempUser']

    # Get all users.
    users = db.users.find()

    return render(request, 'users.html', {'users': users})

def main(request):
    print("get main accessed")
    return HttpResponse('<h1>Hello Http</h1>')