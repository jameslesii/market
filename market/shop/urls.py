from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('categories', views.categories, name="categories"),
    
    path('login/', views.login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('sell/', views.sell, name='sell'),
    path('search/', views.search, name='search'),
    
    path('show_category/<int:pk>', views.show_category, name="show_category"),
    path('show_product/<int:pk>', views.show_product, name="show_product"),
    
    path('users/', views.customers, name='customers'),
    path('user_product/<int:user_id>/', views.user_product, name='user_product'),
    path('messages/<int:msg_id>/',views.messages,name='messages'),
    path('user_messages',views.user_messages,name='user_messages'),
    path('sent_messages',views.sent_messages,name='sent_messages'),
    path('unread_messages',views.unread_messages,name='unread_messages'),
    
    path('conversation/<int:conversation_id>/',views.conversation,name='conversation'),
    path('view_conversations/',views.view_conversations,name='view_conversations'),
    
    path('send_message/<int:recipient_id>/',views.send_message,name='send_message'),
    path('view_message/<int:other_user_id>/',views.view_message,name='view_message'),
    
    path('postjob/',views.postjob,name='postjob'),
    path('jobs/',views.jobs,name='jobs'),
    path('userjobs/<int:user_id>/',views.userjobs,name='userjobs'),
    path('usersjobpost/<int:user_id>/',views.usersjobpost,name='usersjobpost'),
    path('deletejob/<int:job_id>/',views.deletejob,name='deletejob'),
    
    path('sendmsg/',views.sendmsg,name='sendmsg'),
    path('openmsg/<int:conversation_id>/',views.openmsg,name='openmsg'),
    
    path('deletemsg/<int:msg_id>/',views.deletemsg,name='deletemsg'),
    path('deleteproduct/<int:product_id>/',views.deleteproduct,name='deleteproduct'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('deleteAccount/',views.deleteAccount,name='deleteAccount'),

]