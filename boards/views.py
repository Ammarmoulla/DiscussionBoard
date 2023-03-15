from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView, CreateView
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
# Create your views here.

# def home(request):
#     context = {}
#     boards = Board.objects.all()
#     boards_name = []
#     for i in boards:
#         boards_name.append(i.name)
#     html_response = "<br>".join(boards_name)
#     return HttpResponse(html_response)

# def home(request):

#     boards = Board.objects.all()

#     context = {
#         "boards": boards,
#     }
#     return render(request, "boards/home.html", context=context)

class BoardListView(ListView):
    model = Board
    context_object_name = "boards"
    template_name = "boards/home.html"

class TopicListView(ListView):
    model = Topic
    context_object_name = "topics"
    template_name = "boards/topics.html"

    def get_context_data(self, **kwargs):
        kwargs["board"] = self.board
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        board_id = self.kwargs.get("board_id")
        self.board = get_object_or_404(Board, pk=board_id)
        return self.board.topics.order_by("-created_at").annotate(comments=Count("posts"))
            
# def board_topics(request, board_id):
#     context = {}
#     board = get_object_or_404(Board, pk=board_id)
#     queryset = board.topics.order_by("-created_at").annotate(comments=Count("posts"))
#     page = request.GET.get("page", 1)
#     paginator = Paginator(queryset, 20)

#     try:
#         topics = paginator.page(page)

#     except PageNotAnInteger:
#         topics = paginator.page(1)
    
#     except EmptyPage:
#         topics = paginator.page(paginator.num_pages)

#     context = {
#       "board": board,
#       "topics": topics,
#     }
#     return render(request, "boards/topics.html", context=context)

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

    session_key = "view_topic_{}".format(topic.pk)
    if not request.session.get(session_key, False):
        topic.views += 1
        topic.save()
        request.session[session_key] = True
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
            post.updated_by = request.user
            post.updated_at = timezone.now()
            post.save()

            return redirect("topic_posts", board_id, topic.pk)
    context = {
        "form": form,
        "topic": topic
    }

    return render(request, "boards/reply_topic.html", context=context)

@method_decorator(login_required, name="dispatch")
class UpdatePostView(UpdateView):
    model = Post
    fields = ("message", )
    template_name = "boards/edit_post.html"
    context_object_name = "post"
    pk_url_kwarg = "post_id"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect("topic_posts", board_id=post.topic.board.pk, topic_id=post.topic.pk)

