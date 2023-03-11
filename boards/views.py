from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
# Create your views here.

# def home(request):
#     context = {}
#     boards = Board.objects.all()
#     boards_name = []
#     for i in boards:
#         boards_name.append(i.name)
#     html_response = "<br>".join(boards_name)
#     return HttpResponse(html_response)

def home(request):

    boards = Board.objects.all()

    context = {
        "boards": boards,
    }
    return render(request, "boards/home.html", context=context)

def board_topics(request, board_id):
    context = {}
    board = get_object_or_404(Board, pk=board_id)
    topics = board.topics.all()
    context = {
      "board": board,
      "topics": topics,
    }
    return render(request, "boards/topics.html", context=context)

# def new_topic(request, board_id):
    
#     board = get_object_or_404(Board, pk=board_id)

#     if request.method == "POST":
#         subject = request.POST['subject'] # or request.POST.get("subject")
#         message = request.POST['message']
#         user = User.objects.first() # cheak request.POST.get("user")
#         print(subject, message)

#         topic = Topic.objects.create(
#             subject=subject,
#             board=board,
#             created_by=user
#         )
#         post = Post.objects.create(
#             message=message,
#             topic=topic,
#             created_by=user
#         )
#         return redirect('board_topics', board_id=board.pk)
#     context = {
#         "board": board,

#     }

#     return render(request, "boards/new_topic.html", context=context)

@login_required
def new_topic(request, board_id):
    
    board = get_object_or_404(Board, pk=board_id)
    form = NewTopicForm()
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by =request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get("message"),
                topic=topic,
                created_by=request.user
            )
            
            return redirect('board_topics', board_id=board.pk)

    context = {
        "board": board,
        "form": form

    }

    return render(request, "boards/new_topic.html", context=context)



def topic_posts(request, board_id, topic_id):

    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)

    context = {
        "topic": topic,
    }

    return render(request, "boards/topic_posts.html", context=context)


def reply_topic(request, board_id, topic_id):
    
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)
    form = NewPostform()
    if request.method =="POST":
        form = NewPostform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect("topic_posts", board_id, topic.pk)
    context = {
        "form": form,
        "topic": topic
    }

    return render(request, "boards/reply_topic.html", context=context)

