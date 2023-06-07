from django.shortcuts import redirect, render
from . fomrs import *
from django.contrib import messages
from django.views import generic 
# from py  import VideosSearch
from django.contrib.auth.decorators import login_required
import requests
import wikipedia
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
from django.http import HttpResponse,FileResponse

# Create your views here.
def home(request):
    return render(request,'dashboard/home.html') 
def logIn(request):
    if request.method=='POST':
        ii=User.objects.filter(email=request.POST['email']).exists()
        bb=Student.objects.filter(email=request.POST['email'])
        if ii and bb:
         bb=Student.objects.get(email=request.POST['email'])
         pass1=request.POST['pass']
         if bb.password==pass1:
          login(request,authenticate(request,username=bb.username,password=pass1))
          response=redirect('/profile')
          return response
         else:
          messages.error(request,'Passwords do not match !!',extra_tags='error')
        else:
          messages.error(request, "Please Enter A Valid Email",extra_tags='error')
    return render(request,'dashboard/login.html')
def register(request):
    if 'reg' in request.POST:
       
          bb=User.objects.filter(email=request.POST['email']).exists()
          if bb:
            messages.success(request,"Account Already Exists.",extra_tags='error')
          else:
            pass1=request.POST['pass']
            ii=Student(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                password=request.POST.get('pass'),
                username=request.POST.get('user')
            )
            ii.save()
            user=User.objects.create_user(username=request.POST['user'],email=ii.email,
            password=pass1) 
            messages.success(request, "Account Created Successfully !!!",extra_tags='success')  
    return render (request,'dashboard/register.html')
@login_required
def notes(request):
    us=Student.objects.get(email=request.user.email)
    if 'notes' in request.POST:
        dd=Notes.objects.filter(user=us)
        da=len(dd)+1
        cc=Notes(
            noteId=da,
            user=us,
            title=request.POST.get('title'),
            description=request.POST.get('desc')
        )
        cc.save()
        return redirect('/notes')
    if 'delete' in request.POST:
        dd=Notes.objects.get(user=us,noteId=int(request.POST.get('delete')))
        dd.delete()
        return redirect('/notes')
    if 'view' in request.POST:
        dd=Notes.objects.get(user=us,noteId=int(request.POST.get('view')))
        messages.success(request,{'title':'hudai','sub':dd},extra_tags='note')
    cn=Notes.objects.filter(user=us)
    context={
        'notes':cn
    }
    return render(request, 'dashboard/notes.html', context)
@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")
 
class NotesDetailView(generic.DetailView):
    model=Notes
@login_required
def homework(request):
    us=Student.objects.get(email=request.user.email)
    if 'home' in request.POST:
        cc=Homework.objects.filter(user=us)
        aa=len(cc)+1
        dd=Homework(
            user=us,
            subject=request.POST.get('sub'),
            homeworkId=aa,
            title=request.POST.get('title'),
            description=request.POST.get('desc'),
            due=request.POST.get('date')
        )    
        dd.save()
        return redirect('/profile')
    return render(request,'dashboard/homework.html')    
@login_required
def update_homework(request,pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished==True:
        homework.is_finished=False
    else:
        homework.is_finished=True

    homework.save()
    return redirect('homework')    
@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

def youtube(request):
    if request.method=="POST":
        # form=DashboardForm(request.POST)
        # text=request.POST['text']
        # video=VideosSearch(text,limit=20)
        # result_list=[]
        # for i in video.result()['result']:
        #     result_dict={
        #         'input':text,
        #         'title':i['title'],
        #         'duration':i['duration'],
        #         'thumbnail':i['thumbnails'][0]['url'],
        #         'channel':i['channel']['name'],
        #         'link':i['link'],
        #         'viewcount':i['viewCount']['short'],
        #         'publishedTime':i['publishedTime'],
        #     }
        #     desc=''
        #     if i['descriptionSnippet']:
        #         for j in i['descriptionSnippet']:
        #             desc += j['text']

        #     result_dict['description']=desc
        #     result_list.append(result_dict)
        #     context={
        #         'form':form,
        #         'results':result_list
        #     }
        print('something')
        return render(request,'dashboard/youtube.html',context)
    else:
        form=DashboardForm()
    context={'form': form,}
    return render(request,'dashboard/youtube.html',context)

def logOut(request):
   logout(request)
   return redirect('/login')
@login_required
def todo(request):
    if 'create' in request.POST:
        us=Student.objects.get(email=request.user.email)
        aa=len(Todo.objects.filter(user=us))
        if request.POST.get('date'):
            tt=Todo(
                user=us,
                todoId=aa+1,
                title=request.POST.get('title'),
                desc=request.POST.get('desc'),
                date=request.POST.get('date'),
            )
            tt.save()
        else:
            tt=Todo(
                user=us,
                todoId=aa+1,
                title=request.POST.get('title'),
                desc=request.POST.get('desc'),
            )
            tt.save()
        return redirect('/profile')
    return render(request, "dashboard/todo.html")

 
@login_required
def update_todo(request, pk=None):
    
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
         
        todo.is_finished = False
    else:
        todo.is_finished = True
        
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')


def book(request):
    if request.method=="POST":
        form=DashboardForm(request.POST)
        text=request.POST['text']
        url="https://www.googleapis.com/books/v1/volumes?q="+text
        r=requests.get(url)
        answer=r.json()
        
        result_list=[]
        for i in range(10):
            result_dict={
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink')    
            }
             
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/books.html',context)
    else:
        form=DashboardForm()
    context={'form': form}
    return render(request,'dashboard/books.html',context)


def dictionary(request):

    if request.method=="POST":
        form=DashboardForm(request.POST)
        text=request.POST['text']
        url="https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
         

        r=requests.get(url)
        answer=r.json()

        try:
            phonetics=answer[0]['phonetics'][0]['text']
            audio=answer[0]['phonetics'][1]['audio']
            definition=answer[0]['meanings'][0]['definitions'][0]['definition']
            example=answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']

            print(synonyms)
            print(text)
            context={
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms

            }
        except:
              
            
              context={
                'form':form,
                'input':'',
                 

            }
       
        return render(request,'dashboard/dictionary.html',context)

    else:   
        form=DashboardForm()
    context={'form': form}
    return render(request,'dashboard/dictionary.html',context)




def wiki(request):
     if request.method=="POST":
            text=request.POST['text']
            form=DashboardForm(request.POST)
            search=wikipedia.page(text)
            context={
                'form':form,
                'title':search.title,
                'link':search.url,
                'details':search.summary
            }
            return render(request,'dashboard/wiki.html',context)
     else:
        form=DashboardForm()
     context={'form': form}
     return render(request,'dashboard/wiki.html',context)


def conversion(request):
    if request.method=="POST":
        form=ConversionForm(request.POST)
        if request.POST['measuserment']=='length':
            measuserment_form=ConversionLengthForm()
            context={
                'form':form,
                'm_form':measuserment_form,
                'input':True
            }
            if 'input' in request.POST:
                first=request.POST['measure1']
                if(first=='foot'):
                 second='yard'
                else :
                    second='foot'
                print(first)
                input=request.POST['input']
                answer=''
                if input and int(input)>=0:
                    if first=='yard' and second =='foot':
                        answer=f'{input} yard = {int(input)*3} foot' 
                    if first=='foot' and second =='yard':
                        answer=f'{input} foot = {int(input)/3} yard' 
                context={
                    'form':form,
                    'm_form':measuserment_form,
                    'input':True,
                    'answer':answer
                }
            
        if request.POST['measuserment']=='mass':
            measuserment_form=ConversionMassForm()
            context={
            'form':form,
            'm_form':measuserment_form,
            'input':True
        }
            if 'input' in request.POST:
                first=request.POST['measure1']
                if(first=='kilogram'):
                     second='pound'
                else :
                    second='kilogram'
                input=request.POST['input']
                answer=''
                if input and int(input)>=0:
                    if first=='pound' and second =='kilogram':
                        answer=f'{input} pound = {int(input)*0.453592} kilogram' 
                    if first=='kilogram' and second =='pound':
                        answer=f'{input} kilogram = {int(input)*2.20462} pound' 
                context={
                    'form':form,
                    'm_form':measuserment_form,
                    'input':True,
                    'answer':answer
                }

    

    else:
        form=ConversionForm()

        context={
        'form':form,
        'input':False
    }
    return render (request,'dashboard/conversion.html',context)





@login_required
def profile(request):
    us=Student.objects.get(email=request.user.email)
    homeworks=Homework.objects.filter(user=us)
    todos=Todo.objects.filter(is_finished=False,user=us)
    if len(homeworks)==0:
        homework_done=True
    else:
        homework_done=False
    if len(todos)==0:
            todo_done=True
    else:
        todo_done=False
    if 'sub' in request.POST:
        ad=Homework.objects.get(user=us,homeworkId=int(request.POST.get('sub')))
        ad.fil=request.FILES.get('file')
        ad.is_finished=True
        ad.save()
        return redirect('/profile')
    if 'view' in request.POST:
          ad=Homework.objects.get(user=us,homeworkId=int(request.POST.get('view')))
          filepath = os.path.join('media', str(ad.fil))
          return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
    if 'todo' in request.POST:
        dd=Todo.objects.get(user=us,todoId=int(request.POST.get('todo')))
        dd.is_finished=True
        dd.save()
        return redirect('/profile')
    context={
        'homeworks':homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todo_done':todo_done

    }
    return render (request,'dashboard/profile.html',context)
