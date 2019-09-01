from django.shortcuts import render , redirect
from .models import Blog,Comment
from django.core.paginator import Paginator

def index(request): 
    posts = Blog.objects.all()
    paginator = Paginator(posts,3) 
    now_page = request.GET.get('page')
    posts = paginator.get_page(now_page) 
    context={ 
        "posts":posts,  
        }
    return render(request,"index.html",context)

def create(request):

    if request.method == "GET":
        return render(request, 'create.html')
    
    elif request.method == "POST":
        post = Blog()
        post.user = request.user
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.save()
        return redirect(index)

def c_create(request,post_id): # comment create : 댓글 생성&저장 함수
    if request.method == "POST":
        comment = Comment() 
        comment.user = request.user # request.user 는 현재 접속한 유저의 정보
        comment.post = Blog.objects.get(id=post_id) # post_id 는 댓글을 단 post의 id(인증키)
        comment.content = request.POST['comment'] # 'comment'는 text input의 name  
        anonymous = request.POST.get('anonymous',False)  
        if anonymous == "y":
            comment.anonymous = True
        comment.save() 
        return redirect(read,comment.post.id)

def read(request,post_id):
    post = Blog.objects.get(id=post_id)
    comment = Comment.objects.filter(post=post.id)
    context = {
        "post":post,
        "comment":comment,
    }
    return render(request,'read.html',context)

def update(request,post_id):
    if request.method == "GET":
        post = Blog.objects.get(id = post_id)
        context = {
            "post":post,
        }
        return render(request,'update.html',context)

    elif request.method == "POST":
        post = Blog.objects.get(id = post_id)
        post.title = request.POST['title']
        post.content = request.POST['content'] 
        post.save()

        return redirect(index)    
    
    
def delete(request,post_id):

    post = Blog.objects.get(id = post_id_)
    post.delete()

    return redirect(index)


# Create your views here.
