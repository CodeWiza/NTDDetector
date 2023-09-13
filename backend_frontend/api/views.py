import pymongo
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['TempUser']

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





def home(request):
    """
    Create a new user.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        hashed_password = make_password(password)

        user = db.users.find_one({'username': username})

        if user:
            # Retrieve the stored hashed password from the user document
            stored_password = user['password']

            # Hash the input password using the same salt as the stored password
            if check_password(hashed_password, stored_password):
                messages.success(request,"Correct Password") 
                return render(request,  'index.html')  # Passwords match, user is authenticated
            else:
                messages.success(request,"Incorrect Password or User does not exist")  # Passwords do not match
                return redirect('home')

    else:
        return render(request, 'home.html')

def create_user(request):
    """
    Create a new user.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        client = pymongo.MongoClient('mongodb://localhost:27017')
        db = client['TempUser']
        hashed_password = make_password(password)

        existing_user = db.users.find_one({'username': username})
        if existing_user:
            messages.success(request,'Username already exists. Please choose another username or login')
            return render(request, 'create.html')
        # Create a new user document.
        user = {
            'username': username,
            'password': hashed_password,
        }

        db.users.insert_one(user)

        messages.success(request,'User created successfully!')
    return render(request, 'create.html')

def get_users(request):
    """
    Get all users.
    """
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['TempUser']

    # Get all users.
    users = db.users.find()

    return render(request, 'users.html', {'users': users})


def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')

def main(request):
    print("get main accessed")
    return HttpResponse('<h1>Hello Http</h1>')