import pymongo
from django.http import HttpResponse, HttpResponseRedirect
import PIL.Image
import datetime
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# from sorl.thumbnail import ImageField, get_thumbnail



#rendering templates
def login(request):
    return render(request,  'login.html')

def prediction_form(request):
    return render(request, 'prediction_form.html')


def dashboard(request):
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['TempUser']

    # Check to make sure that the `username` key is in the `request.session` dictionary.
    if 'username' not in request.session:
        return render(request, 'Dashboard.html', {'message': 'You must be logged in to view your dashboard.'})

    # Get the username from the `request.session` dictionary.
    username = request.session['username']

    # Use the `MongoDB cursor object` to iterate over the documents in the `user_inputs` collection.
    cursor = db.user_inputs.find({'username': username})

    # Create a list to store the data.
    data = []
    cnt = 1
    # Iterate over the cursor and add each document to the list.
    for document in cursor:
        date = document['date'].get('date')
        time = document['time'].get('time')
        blood_grp = document['blood_group']
        predicted_disease = "XYZ"

        data.append({
            's_no': cnt,
            'date': date,
            'time': time,
            'blood_grp': blood_grp,
            'predicted_disease': predicted_disease,
        })

        cnt += 1

    # Create a context dictionary.
    context = {
        'data': data
    }

    # Render the `Dashboard.html` template, passing in the `context` dictionary.
    return render(request, 'Dashboard.html', context)




@csrf_exempt
def save_data(request):
    if request.method == 'POST':
        blood_group = request.POST['blood_group']
        work_condition = request.POST['work_condition']
        city = request.POST['city']
        age = request.POST['age']
        image = request.FILES['image']

        # image = get_thumbnail(image, '100x100', quality=99, format='JPEG')
        # resize::
        
        new_width=100
        new_height=100

        #converting to byte
        resized_image = PIL.Image.open(image).resize((new_width, new_height))

        # share image now for prediction
        # return HttpResponse({{resized_image}})

        #to store in mongodb
        image_data = resized_image.tobytes()
        
        client = pymongo.MongoClient('mongodb://localhost:27017')
        db = client['TempUser']

        # Get the phone number of the logged in user.
        username = request.session['username']

        # Get the current date and time.
        now = datetime.datetime.now()

        date = now.date()
        date_str = date.isoformat()
        date_dict = dict(date=date_str)

        time = now.time()
        time_str = time.strftime('%H:%M')
        time_dict = dict(time=time_str)

        # Save the data to the MongoDB database.
        user_data = {
            'username': username,
            'blood_group': blood_group,
            'work_condition': work_condition,
            'city': city,
            'age': age,
            'image': image_data,
            'date': date_dict,
            'time': time_dict,
        }

        db.user_inputs.insert_one(user_data)
        
        return HttpResponseRedirect('/dashboard')







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
            messages.success(request,'Username already exists. Please login')
            return render(request, 'login.html')
        # Create a new user document.
        user = {
            'username': username,
            'password': hashed_password,
        }
        request.session['username'] = username
        db.users.insert_one(user)

        messages.success(request,'User created successfully!')
        return HttpResponseRedirect('/dashboard')
    return render(request, 'login.html')

def login_user(request):
    """
    Create a new user.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        client = pymongo.MongoClient('mongodb://localhost:27017')
        db = client['TempUser']
        
        try:

            user = db.users.find_one({'username': username})

            if user: 
                # Retrieve the stored hashed password from the user document
                stored_password = user['password']
                #hashed_password = make_password(password)
                print("Stored Password:", stored_password)
                print("Hashed Input Password:", password)
                # Hash the input password using the same salt as the stored password
                if check_password(password , stored_password):
                    request.session['username'] = username
                    messages.success(request,"Correct Password") 
                    return HttpResponseRedirect('/dashboard')  # Passwords match, user is authenticated
                else:
                    messages.success(request,"Incorrect Password or User does not exist")  # Passwords do not match
                    return render(request, 'login.html')
        except Exception as e:
            messages.error(request, str(e))

    else:
        return render(request, 'login.html')



def logout_user(request):
    logout(request)

    if 'username' in request.session:
        del request.session['username']

    messages.success(request, "You Have Been Logged Out...")
    return HttpResponseRedirect('/')