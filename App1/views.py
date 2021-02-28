from django.shortcuts import render, redirect
import cv2
import pyzbar.pyzbar as pyzbar
import pyqrcode
import random
import datetime
from django.http import HttpResponse
from django.template.loader import get_template

from App1.utils import render_to_pdf

# Create your views here.
from App1.models import register
from django.contrib import messages


def indexPage(request):
    qr = pyqrcode.create('http://127.0.0.1:8000/registerpage')
    # qr = pyqrcode.create('Hello surya')
    qr.png('greet.png', scale=7)
    return render(request, 'index.html')


def registerpage(request):
    if request.method == 'POST':
        name = request.POST['Username']
        mobile = request.POST['phone']
        email = request.POST['email']
        if name:
            if register.objects.filter(name=name).exists():
                # print('User name taken')
                messages.info(request, 'Username Taken')
                return redirect('registerpage')
            elif register.objects.filter(email=email).exists():
                # print('Email Taken')
                messages.info(request, 'Email already taken')
                return redirect('registerpage')
            else:
                user = register.objects.create(name=name, mobile=mobile, email=email)
                frs = datetime.datetime.today()
                Previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)
                # all_user = register.objects.all()
                if frs != Previous_Date:
                    numof_user = register.objects.all().count()
                    print(numof_user)
                    if numof_user <= 20:
                        user.save()
                        print('User Created')
                        messages.info(request, 'Succesfully Registered')
                        getid = register.objects.get(name=name)
                        print(getid.id)

                        return render(request, 'regsiter.html', {'name': name, 'id': getid.id})
                    else:
                        messages.info(request, 'Sorry, Token completed')
                        return redirect('registerpage')

    return render(request, 'regsiter.html')


def qrcode(request):
    # qr = pyqrcode.create('Hey there')
    # qr.png('greet.png', scale=10)
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_PLAIN

    while True:
        _, frame = cap.read()
        l1 = []
        decodedObjects = pyzbar.decode(frame)
        for obj in decodedObjects:
            ans = "Data", obj.data
            print(ans)
            cv2.putText(frame, str(obj.data), (50, 50), font, 2,
                        (255, 0, 0), 3)
            if ans:
                return redirect('registerpage')

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break
    return render(request, 'QrScan.html')


def officepage(request):
    return render(request, 'officePage.html')


def increment(request):
    notify = register.objects.last()
    id1 = notify.id
    ans = id1 - 3
    timing_details = ['Your token number will be arrived within 15min',
                      'Your token number will be arrived within 30min',
                      'Your token number will be arrived within 1hr', 'Your token number will be arrived within 45min',
                      'Your token number will be arrived within 25min',
                      'Your token number will be arrived within 1:30hrs',
                      'Your token number will be arrived within 35min']
    time_choice = random.choice(timing_details)
    print(ans)

    return render(request, 'index.html', {'id': id1, 'ans': ans, 'time': time_choice})

def userinfo(request, *args, **kwargs):
    user_info = register.objects.all()
    print(user_info)
    # template = get_template('userinfo.html')
    # name_info = register.objects.all().values_list('name')
    # email_info = register.objects.all().values_list('email')
    # mobile_info = register.objects.all().values_list('mobile')
    # context = {
    #     'val.name': name_info,
    #     'val.email': email_info,
    #     'val.mobile': mobile_info
    # }
    # html = template.render(context)
    pdf = render_to_pdf('userinfo.html', {'userinfo': user_info})
    return HttpResponse(pdf, content_type='application/pdf')
    # ans = str(user_info)
    # if user_info:
    #     Fileopen = open('user_info.txt', 'w')
    #     Fileopen.write(ans)

    # return render(request, 'userinfo.html', )