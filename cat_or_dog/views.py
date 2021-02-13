from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
import sys
import numpy as np
from .forms import *
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from django.http import HttpResponseRedirect

model = load_model('/home/michu/Pulpit/my_model-cat-dog.h5')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def index(request):
    #return render(request, 'index.html', {'form': form})
    f = '/home/michu/Obrazy/1.jpeg'
    cls_list = ['cats', 'dogs']

    # zaladowanie wytrenowanego modelu
    #net = load_model('./my_model-cat-dog.h5')

    # loop through all files and make predictions
    output = {}
    # Pobranie zdjecia w formacie 224px x 224px
    img = image.load_img(f, target_size=(224,224))
    if img is None:
        print("blad")
        sys.exit(1)
    ## Przetwarzanie obrazu na wstepie, tak jak resnet50
    x = image.img_to_array(img)
    x = preprocess_input(x)
    x = np.expand_dims(x, axis=0)
    # Przewidywanie klasy na podstawie wytrenowanego modelu
    pred = model.predict(x)[0]
    top_inds = pred.argsort()[::-1][:5]
    prediction = {}
    for i in top_inds:
        prediction[i] = '{}'.format(cls_list[i])
        print('{:.3f}{}'.format(pred[i], cls_list[i]))
    return render(request, 'index.html', {'pred': prediction})
