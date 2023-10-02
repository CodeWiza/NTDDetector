import pymongo
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import keras
from django.conf import settings
import os
import numpy as np
import io
import base64
import os
import numpy as np

from keras import backend as K
from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model
import tensorflow as tf
# from sorl.thumbnail import ImageField, get_thumbnail



#rendering templates
def Homepage(request):
    return render(request,  'Homepage.html')

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
        disease1 = document['disease'].get('0')
        
        disease2 = document['disease'].get('1')
        
        probability1 = document['probability'].get('0')

        probability2 = document['probability'].get('1')
        data.append({
            's_no': cnt,
            'date': date,
            'time': time,
            'blood_grp': blood_grp,
            'disease1': disease1,
            'disease2': disease2,
            'probability1': probability1,
            'probability2':probability2,
        })

        cnt += 1

    # Create a context dictionary.
    context = {
        'data': data
    }

    # Render the `Dashboard.html` template, passing in the `context` dictionary.
    return render(request, 'Dashboard.html', context)




import cv2


def convert_ndarray_to_list(ndarray):
    data = []
    for i in range(ndarray.shape[0]):
        data.append( ndarray[i]*100)
    print(data)
    context = {
        'data': data
    }
    return context



def convert_img(img):
    '''
        This function returns the preprocessed and changed dimension of nparray of image passed 
    '''
    img_bytes = io.BytesIO(img.read())
    img = tf.keras.utils.load_img(img_bytes, target_size=(100, 100))
    x = tf.keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

def sort_convert(preds):
    disease = ["Benign", "Malignant"]
    disease=list_to_dict(disease)
    # Get the NumPy array of probabilities
    probabilities = np.array(preds)
    # Sort the probabilities in descending order
    # sorted_probabilities = np.sort(probabilities)[::-1]

    # Get the top 2 probabilities
    # top_2_probabilities = sorted_probabilities[:2]
    # rounded_array = np.around(top_2_probabilities, decimals=2)
    probability= numpy_ndarray_to_dict(probabilities)
    # Get the indices of the top 2 probabilities
    # top_2_indices = np.argsort(probabilities)[::-1][:2]


    # Create a context dictionary
    context = {
        "disease": disease,
        "probability": probability,
    }
    return context

def list_to_dict(list):
    """Converts a list to a dictionary.

    Args:
        list: A list.

    Returns:
        A dictionary.
    """   

    dict = {}
    for i in range(len(list)):
        dict[i] = list[i]
    return dict


def numpy_ndarray_to_dict(ndarray):
  """Converts a NumPy array to a dictionary.

  Args:
    ndarray: A NumPy array.

  Returns:
    A dictionary.
  """

  flattened_array = ndarray.flatten()
  dict = {}
  for i in range(len(flattened_array)):
    dict[i] = np.round(flattened_array[i]*100,2)
  return dict

@csrf_exempt
def save_data(request):
    if request.method == 'POST':
        blood_group = request.POST['blood_group']
        work_condition = request.POST['work_condition']
        city = request.POST['city']
        age = request.POST['age']
        img = request.FILES['image']

        # Load the ML model.
        ML_MODELS_DIR = settings.ML_MODELS_DIR
        model = keras.models.load_model(os.path.join(ML_MODELS_DIR, 'MLmodel.h5'))
        # Convert and preprocess the image file.
        x=convert_img(img)
        preds = model.predict(x)
        context=sort_convert(preds)
        print(context)


        #to store in mongodb
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
        img_bytes = io.BytesIO(img.read())
        img_base64 = base64.b64encode(img_bytes.getvalue()).decode()
        # disease= dict(context['disease_names'])
        # print("disease dict")
        # print(disease)
        # Convert the integer key in the probability dictionary to a string.
        context["probability"] = {str(k): v for k, v in context["probability"].items()}
        context["disease"] = {str(k): v for k, v in context["disease"].items()}
        # Save the data to the MongoDB database.
        user_data = {
            'username': username,
            'blood_group': blood_group,
            'work_condition': work_condition,
            'city': city,
            'age': age,
            'image': img_base64,
            'date': date_dict,
            'time': time_dict,
            'disease': context["disease"],
            'probability': context["probability"]
        }
        print(user_data)
        try:
            db.user_inputs.insert_one(user_data)
        except Exception as e:
            # Handle any errors that may occur.
            print(e)
        
        return HttpResponseRedirect('/dashboard')






#register function
def create_user(request):
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


# login function
def login_user(request):
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


#logout Function

def logout_user(request):
    logout(request)

    if 'username' in request.session:
        del request.session['username']

    messages.success(request, "You Have Been Logged Out...")
    return HttpResponseRedirect('/')