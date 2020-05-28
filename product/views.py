
from .models import Course,Post, Author, PostView,Comment,Follow,Profile
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CommentForm,PostForm,ProfileForm
from django.db.models import Count, Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from notify.signals import notify
from notify.models import Notification,NotificationQueryset
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages




def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            # group=Group.objects.get(name='Customer')
            # user.groups.add(group)
            
            return redirect('/login/')
            
            
    context={'form':form}
    return render(request,'register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
            
    context={}
    return render(request,'login.html',context)
def logoutUser(request):
    logout(request)
    return redirect('/login/')

def get_user_profile(request, username):
    user = User.objects.get(username=username)
    
    featured = Post.objects.filter(featured=True,author=user.id)
    latest = Post.objects.filter(author=user.id).order_by('-timestamp')[0:3]

    try:
        p1=user.profile
        p3=user.profile.first_name
        p2=request.user.profile
        follow=Follow.objects.get(following=p1,follower=p2)
        return render(request, 'profile.html', {"user":user,"follow":follow,"featured":featured,"latest":latest})
    except ObjectDoesNotExist:

    
        return render(request, 'profile.html', {"user":user,"featured":featured})

def follow_user(request, user):
    user = User.objects.get(username=user)
    
    p1=user.profile
    p2=request.user.profile
    follow,created=Follow.objects.get_or_create(following=p1,follower=p2)
    notify.send(request.user, recipient=user, actor=request.user,
                verb='followed you.', nf_type='followed_by_one_user')
    # notify.send(request.user, recipient=user, actor=request.user,
    #             verb='wants to follow you.', nf_type='followed_by_one_user')

    
    
    # return render(request, 'profilefollowing.html', {"user":user})
    return redirect(reverse("product:profile", kwargs={
            'username': user.username
        }))
    # return redirect(reverse("product:profile", kwargs={
    #         'user': profile.user.username}))
def accept_follow(request,user):
    user = User.objects.get(username=user)
    p1=user.profile
    p2=request.user.profile
    follow,created=Follow.objects.get_or_create(following=p2,follower=p1)
    notify.send(request.user, recipient=user, actor=request.user,
                verb='You are following', nf_type='followed_by_one_user')
    
    


def unfollow_user(request, user):
    user = User.objects.get(username=user)
    
    p1=user.profile
    p2=request.user.profile 
    follow=Follow.objects.get(following=p1,follower=p2)
    follow.delete()
    # return redirect('product:profile')
    return redirect(reverse("product:profile", kwargs={
            'username': user.username
        }))
       


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


class SearchView(View):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(overview__icontains=query)
            ).distinct()
        context = {
            'queryset': queryset
        }
        return render(request, 'search_results.html', context)


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search_results.html', context)


def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset

def index(request):
    

    # p2=request.user.profile
    # followed_people = Follow.objects.filter(follower=p2).values('following')
    # featured = Post.objects.filter(featured=True).filter(author__in=followed_people).order_by('-timestamp')[0:3]
    # featured1 = Post.objects.filter(featured=True).exclude(author__in=followed_people).order_by('-timestamp')
    featured = Post.objects.filter(active=True).order_by('-timestamp')
    
    latest = Post.objects.filter(active=True).order_by('-timestamp')[0:3]

    

    context = {
        'object_list': featured,
        'latest': latest,
        # 'object_list1': featured1,
        
    }
    return render(request, 'index.html', context)

def post_list(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    # paginator = Paginator(post_list, 4)
    # page_request_var = 'page'
    # page = request.GET.get(page_request_var)
    # try:
    #     paginated_queryset = paginator.page(page)
    # except PageNotAnInteger:
    #     paginated_queryset = paginator.page(1)
    # except EmptyPage:
    #     paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': post_list,
        'most_recent': most_recent,
        # 'page_request_var': page_request_var,
        'category_count': category_count,
        # 'form': form
    }
    return render(request, 'blog.html', context)
# def post_detail(request, pk):
#     category_count = get_category_count()
#     most_recent = Post.objects.order_by('-timestamp')[:3]
#     post = get_object_or_404(Post, pk=pk)

#     if request.user.is_authenticated:
#         PostView.objects.get_or_create(user=request.user, post=post)

#     form = CommentForm(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             form.instance.user = request.user
#             form.instance.post = post
#             form.save()
#             return redirect(reverse("post-detail", kwargs={
#                 'id': post.pk
#             }))
#     context = {
#         'post': post,
#         'most_recent': most_recent,
#         'category_count': category_count,
#         'form': form
#     }
#     return render(request, 'post.html', context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form = CommentForm()

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        post = self.get_object()
        comments=Comment.objects.filter(reply__isnull=True,post=post).order_by('-timestamp')
        
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        # context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['comments'] = comments
        context['form'] = self.form
        
        return context

    def post(self, request, *args, **kwargs):
        # form = CommentForm(request.POST)
        # if form.is_valid():
        #     post = self.get_object()
        #     form.instance.user = request.user
        #     form.instance.post = post
        #     # form.save()
        #     content=request.POST.get('content')
        #     reply_id=request.POST.get('comment_id')
        #     comment_qs=None
        #     if reply_id:
        #         comment_qs=Comment.objects.filter(id=reply_id)
        #         reply=comment_qs.first()
        #         comment,created=Comment.objects.get_or_create(post=post,user=request.user,content=content,reply=reply)
        #         comment.save()
        
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            post = self.get_object()
            comment_form.instance.user = request.user
            parent_obj = None
            
            try:
                
                parent_id = int(request.POST.get('comment_id'))
            except:
                parent_id = None
            
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                
                if parent_obj:
                    
                    replay_comment = comment_form.save(commit=False)
                    
                    replay_comment.reply = parent_obj
                    replay_comment.post = post
                    replay_comment.user = request.user
            
            new_comment = comment_form.save(commit=False)
          
            new_comment.post = post
            new_comment.user= request.user

            
            new_comment.save()
            return redirect(reverse("product:post-detail", kwargs={
            'slug': post.slug
        }))


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        if self.request.user.is_staff:
            form.instance.active=True
            form.save()
        else:
        
        
        
            messages.info(self.request, "Your Post will be visible shortly")
            form.save()
        return redirect(reverse("product:index"
        ))

class PostCreateStaffView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        if request.user.is_staff:
            form.instance.active=True
        
        form.save()
        # messages.info(self.request, "Your Post will be visible shortly")
        return redirect(reverse("product:index"
        ))


@login_required
# @transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        # user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.instance.user=request.user

            
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profileupdate.html', {
        
        'profile_form': profile_form
    })