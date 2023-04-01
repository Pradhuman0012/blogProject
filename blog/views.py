from django.shortcuts import render,get_list_or_404,get_object_or_404
from blog.models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from blog.forms import EmailSendForm,commentForm
from django.core.mail import send_mail
from taggit.models import Tag
import datetime

# Create your views here.
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])

    paginator=Paginator(post_list,3)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger :
        post_list=paginator.page(1)            
    except:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'blog/post_list.html',{'post_list':post_list,'tag':tag})

def post_detail_view(request,year,month,post):
    post=get_object_or_404(Post,
                        slug=post, 
                        status="published",
                        publish__year=year,
                        publish__month=month
                        )
    comments=post.comments.filter(active=True)
    
    csubmit=False
    if request.method=='POST':
        form=commentForm(request.POST)
        
        
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True    
    else:
        form=commentForm()
    return render(request,'blog/post_detail.html',{'post':post,'form':form,'csubmit':csubmit,'comments':comments})

def EmailSendView(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method=="POST":
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data #dictionary that contain all form data like to form 
            subject=f"{cd['name']}({cd['email']}) recommends you to read {post.title}"
            post_url=request.build_absolute_uri(post.get_absolute_url())
            message=f"Read post At:\n{post_url}\n\nComment:\n{cd['comments']}"
            send_mail(subject,message,'pradhuman@blog.com',[cd['to']])
            sent=True
    else:
        form=EmailSendForm()
    return render(request,'blog/sahrebymail.html',{'form':form,'post':post,'sent':sent})
def trending_post(request):
    return render(request,'blog/trending.html')
