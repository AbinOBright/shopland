from django.shortcuts import render, redirect
from . models import Task
from . forms import TodoForm
from . import views
from django. views.generic import ListView
from django. views.generic . detail import DetailView
from django. views.generic . edit import UpdateView, DeleteView
from django.urls import reverse_lazy


class Tasklistview(ListView):
    model=Task
    template_name ='home.html'
    context_object_name='task1'


class TaskDetailview(DetailView):
    model=Task
    template_name ='detail.html'
    context_object_name='task'

class TaskUpdateview(UpdateView):
    model=Task
    template_name ='update.html'
    context_object_name='task'
    fields=('name','priority','date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class TaskDeleteview(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')


# Create your views here.
def todo(request):
    task = Task.objects.all()
    if request.method=='POST':
        name=request.POST.get('task','')
        priority=request.POST.get('priority','')
        date = request.POST.get('date', '')
        task=Task(name=name, priority=priority, date=date)
        task.save()
        return redirect('/')
    return render(request,'home.html',{'task':task})

def delete(request,id):

    if request.method=='POST':
        task = Task.objects.get(id=id)
        task.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request,id):
    task = Task.objects.get(id=id)
    max =TodoForm(request.POST or None, instance=task)
    if max.is_valid():
        max.save()
        return redirect('/')
    return render(request,'edit.html',{'max':max,'task':task})