from django.forms import ModelForm
from .models import Tag, List, Task, UpdateMessage, Priority, Status
from django.contrib.auth.models import User #django pre defined user class
from django import forms

class TaskForm(forms.ModelForm): 
   # use_required_attribute = False
    class Meta: 
        model = Task 
        fields = '__all__'
        
        exclude = ['completed', 'user',]
        
    deadline = forms.DateTimeField(
        widget=forms.DateInput(
            attrs={'class': 'form-control',
                    'type':"date"}
        )
    )

class TagForm(ModelForm): 
    class Meta: 
        model = Tag 
        fields = '__all__'
        
class ListForm(ModelForm): 
    class Meta: 
        model = List 
        fields = '__all__'        
       
class PriorityForm(ModelForm):  
    class Meta: 
        model = Priority 
        fields = '__all__'   
        