from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from contacts.models import Contact
# Create your views here.
def login(request):
    if request.method =='POST':

        
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username, password=password)
        #user found in databasse
        if user is not None:
            auth.login(request,user)
            messages.success(request,'you are now logged in')
            return redirect('dashboard')
        else:
            messages.success(request,'incorrect credentials')
            return redirect('login')

    else:
        return render(request,'accounts/login.html')


def logout(request):
    if request.method =='POST':
        auth.logout(request)
        messages.success(request,"logged out")
        return redirect('index')


def register(request):
    if request.method =='POST':
        #get form values
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        #check if pass same
        if password == password2:
            # check username
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username already exixts')
                return redirect('register') 
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'email already registered')
                    return redirect('register') 
                else:
                    #everything good
                    user=User.objects.create_user(username=username, password=password,email=email,last_name=last_name,first_name=first_name)
                    #login after register
                    auth.login(request,user)
                    messages.success(request,'you are now logged in')
                    return redirect('dashboard')
                    # or save user
                    #user.save()
                    #messages.success(request,'registered')
                    #return redirect('login')

        else:
            messages.error(request,'Passwords does not match')
            return redirect('register') 



    else:
        return render(request,'accounts/register.html')

def dashboard(request):
    user_contacts=Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context={
        'contacts':user_contacts
    }

    return render(request,'accounts/dashboard.html',context)