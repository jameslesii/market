from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	ProductCategory = models.CharField(max_length=100,null=True,blank=True,
	)
	def __str__(self):
		return(
			f"{self.ProductCategory}"
        )

class County(models.Model):
    countyName = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return (
            f"{self.countyName}"
        )

class Product(models.Model):
    ProductCategory = models.ForeignKey(Category, max_length=100,
                    null=True,blank=True,
                    related_name="category", 
                    on_delete=models.CASCADE
    )
    Owner = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE)
    ProductName = models.CharField(max_length=100,null=True,blank=True)
    ProductImage = models.ImageField( upload_to='images/',null=True,blank=True )
    ProductPrice = models.IntegerField()
    ProductDescription = models.TextField(max_length=1000,null=True,blank=True)
    ProductQuantity = models.IntegerField(null=True,blank=True,default=1)
    ProductLocation = models.CharField(max_length=100,blank=True,null=True)
    ProductDate = models.DateTimeField(auto_now_add=True)
    ProductStatus = models.BooleanField(default=True)
    


    def __str__(self):
        return(
            f"{self.ProductName }" + "  "
            f"{self.Owner}" + "  "
            f"{self.ProductDate}"
            # f"{self.ProductPrice}"
            # f"{self.ProductDescription}"
            # f"{self.ProductQuantity}"
            # f"{self.ProductLocation}"
            # f"{self.ProductStatus}"
            
        )
        
        
class Message(models.Model):
    sender = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE,related_name = 'sent_message')
    receiver = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE,related_name = 'recieved_message')
    product = models.ForeignKey(Product,null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField()
    Timesent = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    
    
    
    def __str__(self):
        return (
            f"{self.content}" + "  "
            f"{self.sender}"  + "  "
            f"{self.receiver}" + "  "
            f"{self.Timesent}" + "  "
            f"{self.status}"
        )
        
class Conversation(models.Model):
    user1 = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='conversation_with_user1')
    user2 = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='conversation_with_user2')
    
    def __str__(self):
        return f"Conversation between {self.user1} and {self.user2}"


class job(models.Model):
    recruiter = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE)
    job = models.CharField(max_length=100, null=True, blank=True)
    jobDescription = models.TextField(null=True,blank=True)
    JobLocation = models.ForeignKey(County,null=True,blank=True,on_delete=models.CASCADE)
    DatePosted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (
            f"{self.job}" + "  "
            f"{self.recruiter}" + "  "
            f"{self.DatePosted}"
        )
    