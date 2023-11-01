from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout

from . forms import LoginForm, SellItemForm, PostJobForm, msgForm
from . forms import UserRegistrationForm
from . models import Category, Product, Message, Conversation, job
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

import os


# Create your views here.

def home(request):
    deleteOld()
    user = request.user
    if user.is_authenticated:
        categories = Category.objects.all()
        products = Product.objects.all()
        
        context = {
            'categories':categories,
            'products':products
        }
        return render(request, 'home.html',context)
    else:
        return redirect('login')

@login_required
def categories(request):
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request, 'categories.html',context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                # Create a new user object but avoid saving it yet
                new_user = user_form.save(commit=False)
                if new_user.first_name == "" or new_user.last_name == "" or new_user.email == "" :
                    return redirect(request.META.get("HTTP_REFERER"))
                else:
                    # Set the chosen password
                    new_user.set_password(user_form.cleaned_data['password'])
                    # Save the User object
                    new_user.save()
                
                return redirect('login')
        else:
            user_form = UserRegistrationForm()
        return render(request,'register.html',{'user_form': user_form})
            
            
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                return redirect('home')
            else:
                
                return redirect('login')

        else:
            return render(request, "login.html")
    
    
@login_required   
def sell(request):
    categories = Category.objects.all().count()
    

    if request.method == 'POST':
        form = SellItemForm(request.POST, request.FILES)
        if form.is_valid():
            ProductCategory = form.cleaned_data['ProductCategory']
            ProductName  = form.cleaned_data['ProductName']
            ProductDescription = form.cleaned_data['ProductDescription']
            ProductPrice = form.cleaned_data['ProductPrice']
            ProductQuantity = form.cleaned_data['ProductQuantity']
            ProductLocation = form.cleaned_data['ProductLocation']
            ProductImage = form.cleaned_data['ProductImage']
            
            ProductStatus = form.cleaned_data['ProductStatus']
           
            item = form.save(commit=False)
            item.Owner = request.user
            item.save()
            
            return redirect('sell')
           
    else:
        form = SellItemForm()
    
    context = {
        'categories':categories,
        
        'form':form,
    }

    
    return render(request,'sell.html', context)
    
@login_required    
def search(request):
    items = Product.objects.all()
    if request.method == "POST":
		# Grab the form field input
        search = request.POST['search']
        # Search the database
        searched = Product.objects.filter(ProductName__contains = search)
        context = {
            'search':search,
            'searched':searched,
            "items":items
            }
        return render(request, 'search.html', context)
    else:
        return render(request, 'search.html', {})
    
@login_required   
def show_category(request, pk):
    categories = Category.objects.all()
    products = Product.objects.all()
    category = get_object_or_404(Category, id=pk)
    context = {
       # 'categories':categories,
        'products':products,
        'category':category
    }
    return render(request, 'show_category.html',context)

@login_required   
def show_product(request, pk):
    products = Product.objects.all()
    product = get_object_or_404(Product, id=pk)
    context = {
        #'products':products,
        'product':product
    }
    return render(request, 'show_product.html',context)

@login_required
def customers(request):
    users = User.objects.all()
    context = {
        "users":users
        }

    return render(request, "customers.html", context)

def user_product(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    products = Product.objects.filter(Owner = user)
    
    context = {
        'user':user,
        'products':products
    }
    return render(request, 'user_products.html', context)

@login_required
def messages(request,msg_id):
    user = request.user
    messages = Message.objects.filter(receiver=user,pk=msg_id)
    messages = messages.order_by('Timesent')
    
    context = {
        'messages':messages
    }
    
    return render(request,'messages.html',context)

@login_required
def user_messages(request):
    user = request.user
    messages = Message.objects.filter(receiver=user)
    messages = messages.order_by('-Timesent')
    
    context = {
        'user':user,
        'messages':messages
    }
    
    return render(request,'user_messages.html',context)

@login_required
def sent_messages(request):
    user = request.user
    messages = Message.objects.filter(sender=user)
    messages = messages.order_by('-Timesent')
    
    context = {
        'user':user,
        'messages':messages
    }
    
    return render(request,'sent_messages.html',context)

@login_required
def unread_messages(request):
    user = request.user
    messages = Message.objects.filter(receiver=user)
    messages = messages.order_by('-Timesent')
    
    context = {
        'user':user,
        'messages':messages
    }
    
    return render(request,'unread_messages.html',context)

#messages between logged in user and the other user
@login_required
def conversation(request, conversation_id):
    user = request.user
    conversations = get_object_or_404(Conversation, id=conversation_id)
    messages = Message.objects.filter(sender=user, receiver=conversations.user1) | Message.objects.filter(sender=user, receiver=conversations.user2) | Message.objects.filter(receiver=user,sender =conversations.user1) | Message.objects.filter(receiver=user,sender =conversations.user2)
    messages = messages.order_by('Timesent')
         
    
    if request.method == 'POST':
        form = msgForm(request.POST)
            
        if form.is_valid():
            msg = form.save(commit=False)
            if request.POST['message'] == "":
                return redirect(request.META.get("HTTP_REFERER"))
            else:
                msg.sender = user
                if Message.sender == conversations.user1:
                    if conversation.user1 == user:
                        Receiver = conversations.user2
                    
                        msg.receiver = Receiver
                        msg.content = request.POST['message']
                        msg.save()
                        return redirect('sent_messages')
                    else:
                        Receiver = conversations.user1
                        
                        msg.receiver = Receiver
                        msg.content = request.POST['message']
                        msg.save()
                        return redirect('sent_messages')
                else:
                    Receiver = conversations.user1
                
                    msg.receiver = Receiver
                    msg.content = request.POST['message']
                    msg.save()
                    
                    return redirect('sent_messages')
           
    else:
        form = msgForm()
    

    context = {
        'user':user,
        'conversations':conversations,
        'messages':messages,
        'form':form      
    }
    
    return render(request, 'conversation_list.html', context)

@login_required
def send_message(request, recipient_id):
    user = request.user
    recipient = User.objects.get(id=recipient_id)
    
    conversation = Conversation.objects.filter(user1=user, user2=recipient).first()
    
    if not conversation:
        conversation = Conversation.objects.create(user1=user,user2=recipient)
        conversation = Conversation.objects.create(user1=recipient,user2=user)
        
    #content = request.POST.get('content')
    #message = Message(sender=user,receiver=recipient)#,content=content)
    #message.save()

    return redirect('conversation',conversation_id=conversation.id)

#chats
@login_required
def view_conversations(request):
    user = request.user
    conversations = Conversation.objects.filter(user1=user)# | Conversation.objects.filter(user2=user)
    context = {
        'user':user,
        'conversations':conversations
    }
    
    return render(request,'conversation.html',context)
        

@login_required
def view_message(request, other_user_id):
    user = request.user
    other_user = User.objects.get(id=other_user_id)
    messages = Message.objects.filter(sender=user,receiver=other_user)|Message.objects.filter(sender=other_user,receiver=user)
    messages = messages.order_by('Timesent')
    
    context = {
        'user':user,
        'other_user':other_user,
        "messages":messages
    }
    
    return render(request,'all_messages.html',context)


@login_required   
def postjob(request):
    if request.method == 'POST':
        form = PostJobForm(request.POST)
        if form.is_valid():            
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            
            return redirect('jobs')
           
    else:
        form = PostJobForm()
    
    context = {
        'form':form
    }

    
    return render(request,'jobpost.html', context)
    
@login_required    
def jobs(request):
    jobs = job.objects.all()
    jobs = jobs.order_by('-DatePosted')
    
    context = {
    'jobs':jobs
    }
    
    return render(request,'jobs.html',context)

@login_required   
def sendmsg(request):
    if request.method == 'POST':
        form = msgForm(request.POST)
        if form.is_valid():            
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            
            return redirect('sent_messages')
           
    else:
        form = msgForm()
    
    context = {
        'form':form
    }

    
    return render(request,'sendmsg.html', context)
    
@login_required    
def openmsg(request, conversation_id):
    user = request.user
        
    messages = Message.objects.filter(receiver=user ,pk=conversation_id) 
    
    for message in messages:
        try:
            conversation = Conversation.objects.filter(user1=message.sender, user2=message.receiver).first()
            conversation_id = conversation.id
            return redirect('conversation',conversation_id)
        except:
            conversation = Conversation.objects.filter(user1=message.receiver, user2=message.sender).first()
            conversation_id = conversation.id
            return redirect('conversation',conversation_id)
       
@login_required    
def deletemsg(request,msg_id):
    user = request.user
    messages = Message.objects.filter(receiver=user,pk=msg_id)
    for message in messages:
        if message.sender != user:
            pass
        else:
            message.delete()
   
    return redirect('user_messages')

# item = get_object_or_404(setupitems,id=item_id)
    
# item.delete()

@login_required
def deleteproduct(request,product_id):
    user = request.user
    products = Product.objects.filter(Owner=user,pk=product_id)
    for product in products:
        if product.Owner == user:
            if product.ProductImage:
                if os.path.isfile(product.ProductImage.path):
                    os.remove(product.ProductImage.path)
                product.delete()
            else:
                product.delete()
                
            return redirect('home')
 
@login_required       
def userjobs(request,user_id):
    user=request.user
    jobs = job.objects.filter(recruiter=user)
    context = {
        'jobs':jobs
    }
    return render(request,'userjobs.html',context)

@login_required 
def usersjobpost(request,user_id):
    jobs = job.objects.filter(recruiter=user_id)
    context = {
        'jobs':jobs
    }
    return render(request,'usersjobpost.html',context)



@login_required
def deletejob(request,job_id):
    user = request.user
    jobs = job.objects.filter(pk=job_id)
    for userjob in jobs:
        if userjob.recruiter == user:
            userjob.delete()
        return redirect('userjobs', user.id)
    


def dashboard(request):
    user = request.user
    if user.is_authenticated:
        context = {
            'user':user
        }
        return render(request,'dashboard.html',context)
    else:
        return redirect('home')
    

from datetime import datetime,timedelta
def deleteOld():
    tendaysold = datetime.now() - timedelta(days=10)
    oldmsg = datetime.now() - timedelta(days=3)
    products_2_delete = Product.objects.filter(ProductDate = tendaysold)
    jobs_2_delete = job.objects.filter(DatePosted = tendaysold)
    deleteoldmsg = Message.objects.filter(Timesent = oldmsg)
    for product in products_2_delete:
        if product.ProductImage:
                if os.path.isfile(product.ProductImage.path):
                    os.remove(product.ProductImage.path)
                product.delete()
        else:
            product.delete()
            
    for jobdel in jobs_2_delete:
        jobdel.delete()
        
    for msg in deleteoldmsg:
        msg.delete()
        
    print('deleted old products , job adverts and messages now')
    print(str(oldmsg)+ " oldmsg")
    print(str(tendaysold)+" tendaysold")

import time   

def deleteAccount(request):
    user = request.user
    if user.is_authenticated:
        user.delete()
        logout(request)
        return redirect('home')
    else:
        return redirect('home')
