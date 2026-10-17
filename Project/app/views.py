from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,auth
# from app.models import registers
# from .models import PublicUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .tasks import *
import os
from django.conf import settings
from django.http import JsonResponse

# Create your views here.
def signin(request):
    if request.method=="POST":
        
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username,password=password)
        if user is not None:
   
            login(request, user)
            messages.success(request,"Login Successfull")
            return redirect('/Dashboard')
        else:
            messages.info(request,'invalid details')
            return redirect('/login')
            
    return render(request,"Login.html",{'hedder':settings.PROJECT_NAME})




def register(request):
    
    if request.method=="POST":
        
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        if User.objects.filter(username=username).exists():
                messages.info(request,"username taken")
                
                return redirect('/')
   
        else:
                user=User.objects.create_user(email=email,username=username,password=password)
                user.save()
                print("user created")
                print(email,username)
        
        return redirect('/login')
        
    return render(request,"Register.html",{'hedder':settings.PROJECT_NAME})




@login_required
def Dashboard(request,page=None):
    if page is None:
        page="Scan"
    else:
        page=page
    if not request.user.is_superuser:
        return render(request,'Dashboard-Main.html',{'page':page,'hedder':settings.PROJECT_NAME})
    else:
        return redirect('signin')


def scan(request):
    isExist = True
    
   
    host = request.POST.get('host')
    user = request.POST.get('user')
    passw = request.POST.get('passw')
    port = request.POST.get('port')
    if port=="":
        port=22

    

    if user !="":
        isExist = os.path.exists(user)
        if passw !="":
            isExist = os.path.exists(passw)
  
    if isExist:
        #task = scan_dir.delay(scan_name,host_name,"/home/kali/Desktop/MiniProject/Directory Brutforcer/Breacher/paths.txt",fast_scan,extension,custom_prefix)
        task = crack.apply_async(args=[host, user,passw,port])
        task_id = task.id
   # print(task.get())
        return JsonResponse({'task_id': task_id})
    else:
        return JsonResponse({'error': "Wordlist Not Found"})


def CheckScanStatus(request):
   task_id = request.GET.get('task_id')
   job = request.GET.get('job')

   if job=='get_scan':
      task = crack.AsyncResult(task_id)


   response_data = {
      'task_id': task_id,
      'status': task.status,
   }
   if task.status == 'SUCCESS':
    
    response_data['result'] = task.result
   return JsonResponse(response_data)


def get_file_list(request):
    base_dir = os.path.dirname(os.path.abspath(__file__))
  
    output_folder_path = os.path.join(base_dir, 'output')

    file_data_list = []

    # Get the list of all files in the "Output" folder
    files = [f for f in os.listdir(output_folder_path) if os.path.isfile(os.path.join(output_folder_path, f))]

    for file_name in files:
        file_path = os.path.join(output_folder_path, file_name)
        with open(file_path, 'r') as file:
            try:
                file_content = json.load(file)
                file_data_list.append({'filename': file_name, 'content': file_content})
            except json.JSONDecodeError:
                # If the file is not a valid JSON, you can handle the error or skip it
                pass

    # Return the list of files and their content as JSON response
    return JsonResponse({'files': file_data_list})

def signout(request):
    logout(request)
    return redirect('signin')