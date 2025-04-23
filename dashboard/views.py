
  
   
from django.shortcuts import render
from .forms import NoteForm,Homework,Todo, HomeworkForm, DashboardForm, TodoForm,ConversionForm, ConversionLengthForm, ConversionMassForm,UserRegistrationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Notes
from django.views import generic 
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/login/')
def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def notes(request):
    # Ensure that user is logged in before creating notes
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:  # Ensure user is logged in
                notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
                notes.save()
                messages.success(request, f"Notes Added by {request.user.username} Successfully")
            else:
                messages.error(request, "You need to be logged in to add notes.")
                return redirect('login')  # Redirect to login if user is not authenticated
    else:
        form = NoteForm()

    # Ensure filtering by user is done only for authenticated users
    if request.user.is_authenticated:
        notes = Notes.objects.filter(user=request.user)
    else:
        notes = Notes.objects.all()  # If not logged in, show all notes or handle differently

    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)

@login_required
def delete_note(request, pk=None):
    try:
        note = Notes.objects.get(id=pk)
        note.delete()  # Deletes the note with the given ID
        messages.success(request, "Note Deleted Successfully")
    except Notes.DoesNotExist:
        messages.error(request, "Note not found")
    return redirect("notes")  # Redirects back to the notes list


class NotesDetailView(generic.DetailView):
    model = Notes
    template_name = 'dashboard/notes_detail.html'


# For Homework
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Homework
from .forms import HomeworkForm
@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST.get('is_finished') == 'on'
            except:
                finished = False

            homeworks = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            homeworks.save()
            messages.success(request, f"Homework Added From {request.user.username}!!")
            return redirect('homework')  # redirect to clear form data after POST
        else:
            # even if POST but invalid form, show errors
            messages.error(request, "There was a problem with your form.")
    else:
        form = HomeworkForm()

    # For GET or after failed POST, show all homeworks and form
    homework = Homework.objects.filter(user=request.user)
    homework_done = len(homework) == 0

    context = {
        'homeworks': homework,
        'homeworks_done': homework_done,
        'form': form,
    }
    return render(request, "dashboard/homework.html", context)


@login_required
def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished == False
    else:
        homework.is_finished == True
        
        homework.save()
        return redirect('homework')



@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")




# for the youtube section 
# def youtube(request):
#     if request.method == "POST":
#         form = DashboardForm(request.POST)
#         if form.is_valid():
#             text = form.cleaned_data['text']
#             video = VideosSearch(text, limit=10)
#             result_list = []

#             for i in video.result()['result']:
#                 result_dict = {
#                     'input': text,
#                     'title': i.get('title'),
#                     'duration': i.get('duration'),
#                     'thumbnail': i.get('thumbnails')[0]['url'] if i.get('thumbnails') else '',
#                     'channel': i.get('channel', {}).get('name'),
#                     'link': i.get('link'),
#                     'views': i.get('viewCount', {}).get('short'),
#                     'published': i.get('publishedTime'),
#                 }

#                 # Fix: variable name was `dec` instead of `desc`
#                 desc = ''
#                 if i.get('descriptionSnippet'):
#                     for j in i['descriptionSnippet']:
#                         desc += j.get('text', '')
#                 result_dict['description'] = desc

#                 result_list.append(result_dict)

#             context = {
#                 'form': form,
#                 'results': result_list
#             }
#             return render(request, 'dashboard/youtube.html', context)

#     else:
#         form = DashboardForm()
        
#     context = {'form': form}
#     return render(request, 'dashboard/youtube.html', context)




def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            video = VideosSearch(text, limit=10)
            result_list = []

            for i in video.result()['result']:
                result_dict = {
                    'input': text,
                    'title': i.get('title'),
                    'duration': i.get('duration'),
                    'thumbnail': i.get('thumbnails')[0]['url'] if i.get('thumbnails') else '',
                    'channel': i.get('channel', {}).get('name'),
                    'link': i.get('link'),
                    'views': i.get('viewCount', {}).get('short'),
                    'published': i.get('publishedTime'),
                }

                # Description snippet handling
                desc = ''
                if i.get('descriptionSnippet'):
                    for j in i['descriptionSnippet']:
                        desc += j.get('text', '')
                result_dict['description'] = desc

                result_list.append(result_dict)

            context = {
                'form': form,
                'results': result_list
            }
            return render(request, 'dashboard/youtube.html', context)

    else:
        form = DashboardForm()
        
    context = {'form': form}
    return render(request, 'dashboard/youtube.html', context)



# for todo:

from django.contrib import messages
@login_required
def todo(request):
    # Handle POST request: when the form is submitted
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            # Get checkbox value for `is_finished` safely
            finished = request.POST.get("is_finished") == "on"

            # Create and save the new Todo item
            todos = Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todos.save()

            # Show success message
            messages.success(request, f"Todo Added by {request.user.username}!")
        else:
            messages.error(request, "Form submission failed. Please try again.")

    # Handle GET request or re-render after POST
    form = TodoForm()  # empty form for new todo
    todo = Todo.objects.filter(user=request.user)  # fetch todos for current user

    # Check if all tasks are completed or no tasks exist
    todos_done = len(todo) == 0

    # Pass context data to template
    context = {
        'form': form,
        'todos': todo,
        'todos_done': todos_done
    }

    return render(request, "dashboard/todo.html", context)


@login_required
def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
        todo.save()
        return redirect('todo')
        
@login_required       
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")


# for books:

import requests  # ← Add this at the top of your views.py file

def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            url = "https://www.googleapis.com/books/v1/volumes?q=" + text
            r = requests.get(url)  
            answer = r.json()
            result_list = []

            for i in range(10):
                item = answer['items'][i]['volumeInfo']
                result_dict = {
                    'title': item.get('title'),
                    'subtitle': item.get('subtitle'),
                    'description': item.get('description'),
                    'count': item.get('pageCount'),
                    'categories': item.get('categories'),
                    'ratings': item.get('averageRating'),
                    'thumbnail': item.get('imageLinks',{}).get('thumbnail'),
                    'preview': item.get('previewLink')
                }
                result_list.append(result_dict)

            context = {
                'form': form,
                'results': result_list
            }
            return render(request, 'dashboard/books.html', context)

    else:
        form = DashboardForm()

    context = {'form': form}
    return render(request, 'dashboard/books.html', context)


# for dictionary:
def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
            r = requests.get(url)  
            answer = r.json()

            try:
                phonetics = answer[0]['phonetics'][0].get('text', '')
                audio = answer[0]['phonetics'][0].get('audio', '')
                definition = answer[0]['meanings'][0]['definitions'][0].get('definition', '')
                example = answer[0]['meanings'][0]['definitions'][0].get('example', '')
                synonyms = answer[0]['meanings'][0]['definitions'][0].get('synonyms', [])

                context = {
                    'form': form,
                    'input': text,
                    'phonetics': phonetics,
                    'audio': audio,
                    'definition': definition,
                    'example': example,
                    'synonyms': synonyms
                }
            except Exception as e:
                context = {
                    'form': form,
                    'input': text,
                    'error': 'Could not find word information. Please check your spelling.'
                }
            return render(request, 'dashboard/dictionary.html', context)

    else:
        # Handle GET request here
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'dashboard/dictionary.html', context)



# for wikipedia:
def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
            
        }
        return render(request,'dashboard/wiki.html',context)
    else:
        form = DashboardForm()
    context ={
        'form':form
    }
    return render(request,'dashboard/wiki.html',context)

# fro connversion:
# def conversion(request):
#     if request.method == "POST":
#         form = ConversionForm(request.POST)
#         if request.POST['measurement'] == 'length':
#             measurement_form = ConversionLengthForm()
#             context = {
#                 'form':form,
#                 'm_form':measurement_form,
#                 'input':True
#             }
#             if 'input' in request.POST:
#                 first = request.POST['measure1']
#                 second = request.POST['measure2']
#                 input = request.POST['input']
#                 answer =''
#                 if input and int(input) >=0:
#                     if first == 'yard' and second == 'foot':
#                         answer = f'{input} yard = {int(input)*3} foot'
#                     if first == 'foot' and second == 'yard':
#                         answer = f'{input} foot = {int(input)/3} yard'
#                         context ={
#                             'form':form,
#                             'm_form':measurement_form,
#                             'input':True,
#                             'answer':answer
#                         }
                    
                    
                    
#             if request.POST['measurement'] == 'mass':
                
#                measurement_form = ConversionMassForm()
#             context = {
#                 'form':form,
#                 'm_form':measurement_form,
#                 'input':True
#             }
#             if 'input' in request.POST:
#                 first = request.POST['measure1']
#                 second = request.POST['measure2']
#                 input = request.POST['input']
#                 answer =''
#                 if input and int(input) >=0:
#                     if first == 'pound' and second == 'kilogram':
#                         answer = f'{input} pound = {int(input)*0.453592} kilogram'
#                     if first == 'kilogram' and second == 'pound':
#                         answer = f'{input} kilogram = {int(input)*2.2062} pound'
#                         context ={
#                             'form':form,
#                             'm_form':measurement_form,
#                             'input':True,
#                             'answer':answer
#                         }
                    
            
#     else:
        
        
#         form = ConversionForm()
#     context = {
#         'form':form,
#         'input':False
#     }
#     return render(request,'dashboard/conversion.html',context)





def conversion(request):
    context = {}
    
    if request.method == "POST":
        form = ConversionForm(request.POST)
        measurement_type = request.POST.get('measurement')
        
        if measurement_type == 'length':
            measurement_form = ConversionLengthForm()
        elif measurement_type == 'mass':
            measurement_form = ConversionMassForm()
        else:
            measurement_form = None

        context = {
            'form': form,
            'm_form': measurement_form,
            'input': True
        }

        if 'input' in request.POST:
            first = request.POST.get('measure1')
            second = request.POST.get('measure2')
            input_value = request.POST.get('input')

            answer = ''
            if input_value and int(input_value) >= 0:
                input_value = int(input_value)

                if measurement_type == 'length':
                    if first == 'yard' and second == 'foot':
                        answer = f'{input_value} yard = {input_value * 3} foot'
                    elif first == 'foot' and second == 'yard':
                        answer = f'{input_value} foot = {input_value / 3:.2f} yard'

                elif measurement_type == 'mass':
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input_value} pound = {input_value * 0.453592:.2f} kilogram'
                    elif first == 'kilogram' and second == 'pound':
                        answer = f'{input_value} kilogram = {input_value * 2.2062:.2f} pound'

                context['answer'] = answer

    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
        }

    return render(request, 'dashboard/conversion.html', context)






def register(request):
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!")
            return redirect("login")
    else:
        form = UserRegistrationForm()  # For GET requests

    context = {
        'form': form
    }
    return render(request, 'dashboard/register.html', context)


@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user=request.user)
    todos = Homework.objects.filter(is_finished=False,user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done=False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done=False
        
    context ={
        'homeworks':homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todos_done':todos_done
    }    
    return render(request,'dashboard/profile.html',context)


def custom_logout(request):
    logout(request)
    return render(request, 'dashboard/logout.html')