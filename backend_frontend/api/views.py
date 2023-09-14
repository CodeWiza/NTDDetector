import pymongo
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
import PIL.Image
import datetime
import bson
# from sorl.thumbnail import ImageField, get_thumbnail


#rendering templates
def index(request):
    return render(request,  'index.html')

def prediction_form(request):
    return render(request, 'prediction_form.html')


def dashboard(request):
    return render(request,'dashboard.html')



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
        phone_number = request.user.phone_number

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
            # 'phone_number': phone_number,
            'blood_group': blood_group,
            'work_condition': work_condition,
            'city': city,
            'age': age,
            'image': image_data,
            'date': date_dict,
            'time': time_dict,
        }

        db.user_inputs.insert_one(user_data)
        # with open('resized_image.png', 'wb') as f:
        #     f.write(resized_image)
        # return HttpResponseRedirect('/dashboard')  
        # return HttpResponse('<h4>image downloaded</h4>')

        # # Redirect to the dashboard route.
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