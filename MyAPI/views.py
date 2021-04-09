from django.shortcuts import render
from rest_framework import viewsets
from . forms import ApprovalForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import  api_view
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib import messages
from rest_framework.parsers import JSONParser
from .models import Approvals
from .serializers import ApprovalsSerializer

import pickle
import joblib
import json
import numpy as np
from sklearn import preprocessing
import pandas as pd
# Create your views here.


class ApprovalsView(viewsets.ModelViewSet):
    queryset  = Approvals.objects.all()
    serializers_class = ApprovalsSerializer


#def myform(request):
#    if request.method == "POST":
#        form = MyForm(request.POST)
#        if form.is_valid():
#            myform = form.save(commit=False)
#    else:
#        form = MyForm()


def encode(df):
    df = df.drop(['csrfmiddlewaretoken'], axis=1)
    df['gpa_high_school'] = df['gpa_high_school'].apply(pd.to_numeric, errors='coerce').dropna()
    encoder = joblib.load('MyAPI/input_encoder.pkl')
    new_df = encoder.transform(df)
    return new_df


def approvereject(request):
    try:
        mdl = joblib.load('MyAPI/model.pkl')
        mydata = request.data
        y_pred = mdl.predict(mydata)
        return y_pred
    except ValueError as e:
        print('meeet error')
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def predict(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        print(type(data))
        serializer = ApprovalsSerializer(data)
        data_receive = serializer.data
        df = pd.DataFrame(data_receive, index=[0])
        province = data_receive['province']
        school = data_receive['school']
        gpa = data_receive['gpa_high_school']
        print(data_receive)
        dict = {'1st':'วิศวกรรมระบบควบคุม',
                '1st_percent':'80.8',
                '2rd':'วิศวกรรมตมนาคม',
                '2st_percent': '70.8',
                '3st':'วิศวกรรมอาหาร',
                '3st_percent': '55.8',
        }
        #json_object = json.dumps(dict, ensure_ascii=False)
        #print(type(json_object))
        return JsonResponse(dict)


def cxcontact(request):
    if request.method == 'POST':
        form = ApprovalForm(request.POST)
        if form.is_valid():
            print(form)
            school = form.cleaned_data['school']
            department = form.cleaned_data['department']
            faculity = form.cleaned_data['faculity']
            # gender = form.cleaned_data['gender']
            province = form.cleaned_data['province']
            gpa_high_school = form.cleaned_data['gpa_high_school']
            print(request.POST)
            myDict = (request.POST).dict()
            df = pd.DataFrame(myDict, index=[0])
            new_df = encode(df)
            print('this is new_df')
            prediction = approvereject(new_df)
            print('this is prediction ', prediction)
            messages.success(request, 'Prediction score:{}'.format(prediction))

    form = ApprovalForm()
    return render(request,'myform/cxform.html', {'form':form})
