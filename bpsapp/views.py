from django.shortcuts import render,redirect
from django.views.generic import *
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth import logout, authenticate, login
from .forms import RegistrationForm,LoginForm,ReviewForm,ReplyForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from  bpsapp.Recommendation import KNN.py 



def Visitorhome_view(request):

	return render(request,'visitortemplates/visitorhome.html',{})

def registration_view(request):
	form=RegistrationForm()

	if request.method=='POST':
		form=RegistrationForm(request.POST)

		if form.is_valid():
			a=form.cleaned_data["username"]
			b=form.cleaned_data["email"]
			c=form.cleaned_data["password"]
			user = User.objects.create_user(username=a, email=b, password=c)
			form.instance.user=user
			form.save()
			return redirect('bpsapp:login')

	else:
		form=RegistrationForm()
	return render(request,"visitortemplates/visitorregistration.html",{'form':form})

def login_view(request): 

    form=LoginForm()
    if request.method=='POST':
        form=LoginForm(request.POST,request.FILES or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username)
            print(password)
            


            user1 = authenticate(request,username=username,password=password)
            print(user1)


            if user1 is not None:
                print(user1)
                
                login(request,user1)
                print('login successfull')
                return HttpResponseRedirect(reverse('bpsapp:visitorhome'))

                
    else:
       form=LoginForm()
    return render(request,'visitortemplates/visitorlogin.html',
                {'form':form,
                  "error": "Invalid username or password"})  

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")                  		
    

def location_view(request):

    location=Location.objects.all()
    category=LocationCategory.objects.all()
    
    context={
     'location':location,
     'category':category,
    
     
    }
    return render(request,'visitortemplates/location.html',context)

@login_required
def locationdetail_view(request,detail_pk):
    form=ReviewForm()
    replyform=ReplyForm()
    locationdetail=Location.objects.get(id=detail_pk)
    category=locationdetail.category.all()
    print(category)
    review=LocationReview.objects.all()
   
  
    context={
     'form':form,
     'location':locationdetail,
     'review':review,
     'replyform':replyform,
     'categorys':category,
    
    
     
      

    }

    return render(request,'visitortemplates/locationdetail.html',context)



@login_required
def locationreview_view(request,location_pk):
    form=ReviewForm()
    if request.method=='POST':
     form=ReviewForm(request.POST)
     if form.is_valid():
        form.instance.location=Location.objects.get(id=location_pk)
        logged_in_user=User.objects.get(username=request.user.username) #Mistake: BlogForm() ko model 'Article' ho jasma ma 'author' vanne field xa 'visitor' vanne xaina ni. tesaile 'form.instance.author' garnu parxa not 'form.instance.visitor'
        print(logged_in_user) 
        visitor=Visitor.objects.get(user=logged_in_user)
        form.instance.commenter=visitor
        form.save()
        return HttpResponseRedirect(reverse('bpsapp:locationdetail',kwargs={'detail_pk':location_pk}))

    else:
        form=ReviewForm()
        location=Location.objects.get(id=location_pk)
        context = {
         'form':form,
         'article':article,
            
        } 

    return render(request,"visitortemplates/locationdetail.html",context)

@login_required
def locationreviewdelete_view(request,reviewdelete_pk):
    comment_obj=LocationReview.objects.get(id=reviewdelete_pk)
    commenter=comment_obj.commenter
    location_id=comment_obj.location.id

    if request.user.is_authenticated and request.user==commenter.user:
        print(comment_obj)
        comment_obj.delete()

    else:
       print("user is not commenter")

    return HttpResponseRedirect(reverse('bpsapp:locationdetail',kwargs={'detail_pk':location_id}))          











    

