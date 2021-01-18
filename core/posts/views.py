from django.shortcuts import render, redirect
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView,DeleteView
from django.urls import reverse_lazy
from .models import Post,Like
from django.contrib import messages

# Create your views here.

def post_comment_create_and_list_view(request):
    all_posts = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    
    post_form = PostModelForm()
    comment_form = CommentModelForm()
    post_added = False
    
    profile = Profile.objects.get(user=request.user)
    
    if "submit_post_form" in request.POST:
        #print(request.POST)
        post_form = PostModelForm(request.POST ,request.FILES)
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.author = profile
            instance.save()
            post_form = PostModelForm()
            post_added = True   
        
    if "submit_comment_form" in request.POST:
        #print(request.POST)
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            
            comment_form = CommentModelForm()   
        
     
    
    
    context = {
        'all_posts' : all_posts,
        'profile' : profile,
        'post_form': post_form,
        'comment_form' : comment_form, 
        'post_added' : post_added,
    }
    return render(request, 'posts/main.html',context)

def like_unlike_post(request):
    user = request.user

    if request.method =='POST':
        post_id = request.POST.get('post_id')
        profile = Profile.objects.get(user=user)
        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
        post_obj = Post.objects.get(id=post_id)
        
        
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
            
        else:
            post_obj.liked.add(profile)
            
        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
        
        if not created:
            if like.value =='Like':
                like.value='Unlike'
            else:
                like.value='Like'
                
            post_obj.save()
            like.save()
        else:
            like.value='Like'
    
    
    return redirect('posts:main-view')   

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostModelForm
    template_name = 'posts/post-update.html'
    success_url = reverse_lazy('posts:main-view')
    
    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        
        else:
            form.add_error(None,'Only this post author can update it')
            return super().form_invalid(form)
            
    

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post-delete.html'
    success_url = reverse_lazy('posts:main-view')
    #success_url = '/posts/'
     
    def get_post(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post_obj = Post.objects.get(pk=pk)
        if not post_obj.author.user == self.request.user:
            messages.warning(self.request, 'Only this post author can delete it')
        return post_obj
     
        
        