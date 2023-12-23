from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .email import send_otp_via_email
# Create your views here.
def index(request):
    return render(request, 'index.html')

def home1(request):
    return render(request, 'home1.html')

"""
def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']
    user = request.user
    username1 = user.username
    if username==username1:
        if Room.objects.filter(name=room).exists():
            return redirect('/'+room+'/?username='+user.first_name)
        else:
            new_room = Room.objects.create(name=room)
            new_room.save()
            return redirect('/'+room+'/?username='+user.first_name)
    else:
        messages.info(request,'wrong username')
        return redirect('home1')

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    ok = 0
    for s in message:
        if s != " ":
            ok=1
            break
    if message != "" and ok:
        new_message = Message.objects.create(value=message, user=username, room=room_id)
        new_message.save()
        return HttpResponse('Message sent successfully')
    else:
        return HttpResponse('Unable to send')
def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})
"""
#user account

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        passward=request.POST['password']
        user = auth.authenticate(username=username, password=passward)    
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'wrong username or password')
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        passward1=request.POST['password1']    
        passward2=request.POST['password2']    
        
        if passward1==passward2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username, password=passward1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                print('user created')
                return redirect('login')
        else:
            messages.info(request,'passward not matching')
            return redirect('register')
    else:
        return render(request, 'register.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')

class CreateTotalBudget(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        total_amount = request.data.get('total_amount')
        savings_goal = request.data.get('savings_goal')
        start_date = request.data.get('start_date')
        user = User.objects.get(username=username)
        TotalBudget.objects.create(owner=user, total_amount=total_amount, savings_goal=savings_goal, start_date=start_date)
        return Response({
            'status': True,
            'message': 'Budget created successfully'
        }, status=status.HTTP_200_OK)

class GetTotalBudget(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        user = User.objects.get(username=username)
        budget = TotalBudget.objects.get(owner=user)
        total_amount = budget.total_amount
        savings_goal = budget.savings_goal
        start_date = budget.start_date
        expances = DailyExpance.objects.filter(owner=user)
        used_amount = 0
        for expance in expances:
            used_amount += expance.amount
        remaining_amount = total_amount - used_amount
        return Response({
            'status': True,
            'message': 'Budget details',
            'total_amount' : total_amount,
            'savings_goal' : savings_goal,
            'start_date' : start_date,
            'remaining_amount' : remaining_amount,
            'used_amount' : used_amount
        }, status=status.HTTP_200_OK)

class CreateDailyExpance(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        amount = request.data.get('amount')
        date = request.data.get('date')
        user = User.objects.get(username=username)
        DailyExpance.objects.create(owner=user, amount=amount, date=date)
        expances = DailyExpance.objects.filter(owner=user)
        used_amount = 0
        for expance in expances:
            used_amount += expance.amount
        budget = TotalBudget.objects.get(owner=user)
        total_amount = budget.total_amount
        savings_goal = budget.savings_goal

        if total_amount-savings_goal < used_amount:
            mail = user.email
            send_otp_via_email(mail, used_amount)

        return Response({
            'status': True,
            'message': 'Daily expance created successfully'
        }, status=status.HTTP_200_OK)

class GetDailyExpance(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        user = User.objects.get(username=username)
        expances = DailyExpance.objects.filter(owner=user)
        data = []
        for expance in expances:
            val = {}
            val['amount'] = expance.amount
            val['date'] = expance.date
            data.append(val)
        return Response({
            'status': True,
            'message': 'daily expances',
            'data': data
        }, status=status.HTTP_200_OK)