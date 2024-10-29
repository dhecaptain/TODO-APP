from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q
from .models import Todo
from .forms import TodoForm
from django.utils import timezone
import csv
from django.http import HttpResponse
from django.db.models import Count

# Create your views here.
def index(request):
    sort_by = request.GET.get('sort','-date')
    valid_sort_fields = {
        'date':'date',
        '-date':'-date',
        'priority':'priority',
        'status':'status',
        'due_date':'due_date',
        'title':'title'
    }
    sort_fields = valid_sort_fields.get(sort_by,'-date')

    item_list = Todo.objects.all()

    #Search functionality
    search_query = request.GET.get('search','')
    status_filter = request.GET.get('status','')
    priority_filter = request.GET.get('priority','')

    if search_query:
        item_list = item_list.filter(
            Q(title__icontains=search_query) |
            Q(details__icontains=search_query)
        )
    
    if status_filter:
        item_list = item_list.filter(status=status_filter)
    
    if priority_filter:
        item_list = item_list.filter(priority=priority_filter)

    # Apply sorting
    item_list = Todo.objects.order_by(sort_fields)

    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Task added successfully!')
            return redirect('todo')
    else:
        form = TodoForm()
    
    # Statistics
    context = {
        'forms': form,
        'list':item_list,
        'title': "TODO LIST",
        'status_filter':status_filter,
        'search_filter':search_query,
        'priority_filter':priority_filter,
        'total_tasks':Todo.objects.count(),
        'completed_tasks':Todo.objects.filter(status='COMPLETED').count(),
        'pending_tasks':Todo.objects.filter(status='PENDING').count(),
        'high_priority':Todo.objects.filter(priority='HIGH').count(),
        'due_today':Todo.objects.filter(
            due_date__date=timezone.now().date()
        ).count(),
        'overdue':Todo.objects.filter(
            due_date__lt=timezone.now(),
            status__in=['PENDING','IN_PROGRESS']
        ).count(),
        'category_stats':Todo.objects.values('category__name').annotate(count=Count('id'))
    }
    context['now'] = timezone.now() 
    
    # Add overdue tasks count
    context['overdue_tasks'] = item_list.filter(
        due_date__lt=timezone.now(),
        status__in=['PENDING', 'IN_PROGRESS']
    ).count()
    return render(request, 'todo/index.html',context)

def remove(request,item_id):
    item = Todo.objects.get(id=item_id)
    item.delete()
    messages.info(request,'Item removed !!!')
    return redirect('todo')

def done(request,item_id):
    task = Todo.objects.get(id=item_id)
    if task.status == 'COMPLETED':
        task.status = 'PENDING'
    else:
        task.status = 'COMPLETED'
    task.save()
    messages.success(request,f'Task "{task.title}" status updated successfully!')
    return redirect('todo')

def export_tasks(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Details', 'Date Created', 'Due Date' 'Priority', 'Status','Category','Tags'])
    tasks = Todo.objects.all()
    for task in tasks:
        writer.writerow([task.title,
                        task.details,
                        task.date,
                        task.due_date,
                        task.get_priority_display(),
                        task.get_status_display(),
                        task.category.name if task.category else '',
                        task.tags
                    ])
    return response