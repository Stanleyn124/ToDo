from django.db import models
from django.contrib.auth.models import User #django pre defined user class

class Tag(models.Model):
    tag = models.CharField(max_length=70)
    
    def __str__(self):
        return self.tag   
   

class List(models.Model): # what list the topics will be in, basically groups
    name = models.CharField(max_length=70)
    
    def __str__(self):
        return self.name    

class Priority(models.Model): # 
    priority = models.CharField(max_length=70)
    tag_color_type = models.CharField(max_length=70, null=True)
    
    def __str__(self):
        return self.priority   
    
class Status(models.Model): # 
    status = models.CharField(max_length=70)
    
    def __str__(self):
        return self.status  
    
           
class Task(models.Model): #consider adding feature later where you can add sub tasks to tasks
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    list = models.ForeignKey(List, on_delete=models.SET_NULL, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True) #null is allowed otherwords this can be blank

    

    update = models.DateTimeField(auto_now=True) # This will take time stamps automatically
    created = models.DateTimeField(auto_now_add=True) # auto_now_add this will be the initial time stamp. so maybe when a room was created
    completed = models.DateTimeField(null=True, blank=True) 
    #^based on status most likely....
    deadline = models.DateTimeField(null=True, blank=True) 
    
   
    def __str__(self):
        return self.name
    
class UpdateMessage(models.Model): # will allow user to make comments and updates on their Task 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE) # on_delete=models.CASCADE when a room is deleted all the messages (children) will be deleted
    body = models.TextField() 
    update = models.DateTimeField(auto_now=True) # This will take time stamps automaticallyt 
    created = models.DateTimeField(auto_now_add=True) # auto_now_add this will be the initial time stamp. so maybe when a room was created
    class Meta: 
        ordering = ['-update', '-created'] 
            
    def __str__(self):
        return self.body #[0:50] #this gets the first 50 characters