from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tag, List, Task, UpdateMessage, Priority, Status
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import TaskForm, TagForm, ListForm, PriorityForm
from django.db.models import Q # this will import query stuff to wrap queries
from datetime import datetime


# def createUser(request):
#     form = MyUserCreationForm()

#     if request.method == 'POST':
#         form = MyUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save()
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'An error occurred during registration')

#     return render(request, 'base/field_form.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' # empty string is home page so if there's no slug the default will be   
    q_task = request.GET.get('q_task') if request.GET.get('q_task') != None else ''
    tasks = Task.objects.filter(
        Q(tag__tag__icontains = q) | # |   the | means OR 
        Q(list__name__icontains = q) |
        Q(priority__priority__icontains = q) |
        Q(status__status__icontains = q) | 
        Q(name__icontains = q)
        )
    
    task_messages = UpdateMessage.objects.filter(
        Q(task__tag__tag__icontains = q) | # |   the | means OR 
        Q(task__list__name__icontains = q) |
        Q(task__priority__priority__icontains = q) |
        Q(task__status__status__icontains = q)
        )
    
    priority_completed = Task.objects.filter(
        Q(status__status__icontains = q_task) 
        
        )
    # results = request.GET['fruits']
    # print('this is the fruits')
    # print(results)


    # tasks_completed = Task.objects.filter(
    #     Q(status__exact = q_task) 
    #     )
    
    # messages_task_id = task_messages.task
    # name_task = Task.objects.get(name=messages_task_id)
    
    # taskobj = Task.objects.filter(Q(name__icontains = name_task))
    
    #tasks = Task.objects.all()
    tags = Tag.objects.all()
    lists = List.objects.all()
    prioritys = Priority.objects.all()
    statuss = Status.objects.all()
    
    tags_count = tags.count()
    lists_count = lists.count()
    prioritiy_count = prioritys.count()
    tasks_count = tasks.count()
    
    
    context = {'tasks':tasks, 'tags':tags, 'lists':lists,
               'prioritys':prioritys, 'task_messages':task_messages,
                'statuss':statuss, 'priority_completed':priority_completed,
                'tags_count':tags_count, 'lists_count':lists_count, 
                'prioritiy_count':prioritiy_count, 'tasks_count':tasks_count } # 'tasks_completed':tasks_completed,
    
    return render(request, 'base/home.html', context)


def createMessage(request, pk):


    task = Task.objects.get(id=pk)

    if request.method == 'POST':
        message = UpdateMessage.objects.create(
            user=request.user,
            task=task,
            body=request.POST.get('body')
        )
        
    return render(request, 'base/task.html', {})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = UpdateMessage.objects.get(id=pk)
    message_task_id = message.task
    name_task = Task.objects.get(name=message_task_id)
    
    taskobj = Task.objects.filter(
        Q(name__icontains = name_task))
    taskobj_id = taskobj[0].id

    tasks = Task.objects.all()
    print("taskobj")
    print(taskobj_id)
    

   
   # idd = task_obj.objects.get(id)
    if request.user != message.user: # if they are not the owner of the message
        # return HttpResponse('You are not allowed here')
        reason_message = "Hey guess what? Since you are not logged in"
        message_underline = "you are NOT allowed in here!"

        context = {'reason_message':reason_message, 'message_underline':message_underline, 'name_task':name_task, 'taskobj':taskobj,
        'tasks':tasks}

        
        return render(request, 'base/not_allowed_here.html', context)
    
    if request.method == 'POST':
        
        message.delete()
        
        pk_task = taskobj_id
        return redirect('home')
        
    return render(request, 'base/delete_message.html', {'obj':message, 'taskobj_id':taskobj_id})


def task(request, pk): 
    task = Task.objects.get(id=pk) 
    task_messages = task.updatemessage_set.all().order_by('created') #model name is always lowercase. this will give us the set of messages that are related to this room
    
    statuss = Status.objects.all()
    
    if request.method == 'POST': 
        message = UpdateMessage.objects.create(
            user = request.user,
            task = task,
            body=request.POST.get('body')
            
        )
        
        print("testing body")
        return redirect('task', pk=task.id)
    
    context = {'task':task, 'task_messages':task_messages, 'statuss':statuss}
    
    return render(request, 'base/task.html', context)

@login_required(login_url='login') # this will require that a user is logged in to create a room and redirect them to login page
def createTask(request):
    form = TaskForm()
    
    if request.method =='POST': 
        
        Task.objects.create(
            user = request.user,
            # tag=request.POST.get('tag'),
            # list=request.POST.get('list'),
            # priority=request.POST.get('priority'),
            # status=request.POST.get('status'),
            description=request.POST.get('description'),
            name=request.POST.get('name'),
            # deadline=request.POST.get('deadline'),
        )
    
        return redirect('home') 
    context = {'form':form}
    
    return render(request, 'base/field_form.html', context)


@login_required(login_url='login') # this will require that a user is logged in to create a room and redirect them to login page
def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(request.POST or None, instance = task)

    tags = Tag.objects.all()
    lists = List.objects.all()
    prioritys = Priority.objects.all()
    statuss = Status.objects.all()

    # for key, value in statuss.items():
    #     pass
    # print(value)

    
    if request.user != task.user: # if they are not the owner
        reason_message = "Hey guess what? Since you are not logged in"
        message_underline = "you are NOT allowed in here!"

        context = {'reason_message':reason_message, 'message_underline':message_underline}
        return render(request, 'base/not_allowed_here.html', context)

    if request.method =='POST':

        list_task = request.POST.get('list_task')
        list_task_list, created = List.objects.get_or_create(name=list_task)
        task.list = list_task_list

        tag_label = request.POST.get('tag_label')
        status_task_tag, created = Tag.objects.get_or_create(tag=tag_label)
        task.tag = status_task_tag

        status_task = request.POST.get('status_task')
        status_task_status, created = Status.objects.get_or_create(status=status_task)
        task.status = status_task_status

        desc_body = request.POST.get('desc_body')
        task.description = desc_body

        task.save()
        return redirect('home')

        print("here is the list: ")
        print(list_task)

        print("here is the tag_label: ")
        print(tag_label)

        print("here is the status_task: ")
        print(status_task)
        

        print("printing request method here!")
        print(request) 
       

    context = {'form':form, 'task':task, 'tags':tags, 'lists':lists, 'prioritys':prioritys, 'statuss':statuss}
    
    return render(request, 'base/task.html', context)


@login_required(login_url='login')
def deleteTask(request, pk):
    task = Task.objects.get(id=pk)


    # reason_message = "Hey guess what? Since you are not logged in"
    #     message_underline = "you are NOT allowed in here!"

    #     context = {'reason_message':reason_message, 'message_underline':message_underline, 'name_task':name_task, 'taskobj':taskobj,
    #     'tasks':tasks}

        
    #     return render(request, 'base/not_allowed_here.html', context)


    
    if request.user != task.user: # if they are not the owner
        reason_message = "Hey guess what? Since you are not logged in"
        message_underline = "you are NOT allowed in here!"


        context = {'reason_message':reason_message, 'message_underline':message_underline}
        return render(request, 'base/not_allowed_here.html', context)
    
    if request.method == 'POST':
        task.delete()
        return redirect('home')
    
        context = {'obj':task}
        return render(request, 'base/delete.html', context)


def createTag(request):
    form = TagForm()
    if request.method =='POST': 
        
   
        Tag.objects.create(
            tag=request.POST.get('tag'),
        )
    
        return redirect('home') 
    context = {'form':form}
    
    return render(request, 'base/create_tag_form.html', context)


def updateTag(request, pk):
    tag = Tag.objects.get(id=pk)
    form = TagForm(request.POST or None, instance = tag)
   
    if request.method =='POST': 
        if form.is_valid:
            form.save()
            
        return redirect('home')

    context = {'form':form}
    
    return render(request, 'base/field_form.html', context)


def createList(request):
    form = ListForm()
    if request.method =='POST': 
        
        List.objects.create(
            name=request.POST.get('name'),
        )
    
        return redirect('home') 
    context = {'form':form}
        
    return render(request, 'base/field_form.html', context)


def updateList(request, pk): #NEED TO UPDATE TO MANY TO MANY FOR TAG AND LISTS!!!!!!!!!!
    list = List.objects.get(id=pk)
    form = ListForm(request.POST or None, instance = list)
   
    if request.method =='POST': 
        if form.is_valid:
            form.save()
            
        return redirect('home')

    context = {'form':form}
    
    return render(request, 'base/field_form.html', context)


def createPriority(request): 
    form = PriorityForm()
    priority_names_num = Priority.objects.get(tag_color_type = 'badge rounded-pill bg-danger')
    tracker = 0
    print("tracker is: " + str(tracker))
    prioritys = Priority.objects.all()

    print('method is: ')
    print(request.method)
    # name_task = Task.objects.get(name=message_task_id)

    checkboxes =  request.GET.getlist("checkbox")
    print("check box list")
    print(checkboxes)
    


    if request.method =='GET' or request.method =='POST': 
        tracker = 1
        print("tracker after GET " + str(tracker))
        existing_priority = request.GET.get('priority_text_submit')
        print(existing_priority)

        print("hi")

        num_results = Priority.objects.filter(priority = str(existing_priority)).count()
        print(num_results)


        context = {'existing_priority':existing_priority, 'num_results':num_results, 'tracker':tracker,
        'form':form, 'priority_names_num':priority_names_num, 'prioritys':prioritys} 
        
        if request.method =='GET':
            return render(request, 'base/create_priority_form.html', context)
        elif request.method =='POST':
            if num_results == 1:
            
                Priority.objects.create(
                    priority=request.POST.get('priority')
                )
                return redirect('home') 
        # check to see if priority name already exists if it does, submit 

        states = request.GET.getlist('checkbox')
        print("test")
        print(states)
        


    # if request.method =='GET': 
    #     name_task = request.GET('priority_text_submit')     Task.objects.get(name=message_task_id)



        
    
def createnewPriority(request): 
    form = PriorityForm()
    prioritys = Priority.objects.all()
    
    

    #num_results = User.objects.filter(email = cleaned_info['username']).count()

    priority_names_num = Priority.objects.filter(priority == 'badge rounded-pill bg-danger')

    if request.method =='POST': 

        #check to see if something has been selected and only 1 item has been selected 
            #if not throw input error with a variable        input_error_var = false / true


        #check to see if there is an existing name 
        # if priority_names_num > 0:
        #     #name exists
        # else:
        #     #name doesn't exist
        
        
        Priority.objects.create(
            priority=request.POST.get('priority'),
            tag_color_type=request.POST.get('tag_color_type'),
        )
    # check to see if priority name already exists if it does, submit 
    
        return redirect('home') 
    context = {'form':form, 'priority_names_num':priority_names_num}
        
    return render(request, 'base/create_priority_form.html', context)
    


def updatePriority(request, pk): 
    priority = Priority.objects.get(id=pk)
    form = PriorityForm(request.POST or None, instance = priority)
   
    if request.method =='POST': 
        if form.is_valid:
            form.save()
            
        return redirect('home')

    context = {'form':form}
    
    return render(request, 'base/field_form.html', context)  