import pymongo
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required


#rendering templates
def index(request):
    return render(request,  'index.html')

def prediction_form(request):
    return render(request, '')


def dashboard(request):
    return render(request,'')




@csrf_exempt
@login_required
def save_data(request):
    if request.method == 'POST':
        blood_group = request.POST['blood_group']
        work_condition = request.POST['work_condition']
        city = request.POST['city']
        age = request.POST['age']
        image = request.FILES['image']
        
        client = pymongo.MongoClient('mongodb://localhost:27017')
        db = client['TempUser']

        # Get the phone number of the logged in user.
        phone_number = request.user.phone_number

        # Save the data to the MongoDB database.
        user_data = {
            'phone_number': phone_number,
            'blood_group': blood_group,
            'work_condition': work_condition,
            'city': city,
            'age': age,
            'image': image,
        }

        db.user_inputs.insert_one(user_data)

        # Redirect to the dashboard route.
        return HttpResponseRedirect('/dashboard')







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