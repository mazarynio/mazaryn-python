from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileModelForm
from .models import Profile, Relationship
from django.views.generic import ListView ,DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProfileSerializer ,RelationshipSerializer
from rest_framework import viewsets

# Create your views here.


@login_required
@api_view(['GET', 'POST','HEAD'])
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST, request.FILES or None, instance=profile)
    update_flag = False
    
    if request.method == 'GET':
        if form.is_valid():
            form.save()
            update_flag = True

        
    context = {
        'profile': profile,
        'form': form,
        'update_flag': update_flag

    }
    return render(request, 'profiles/myprofile.html', context)



# @login_required
# @api_view(['GET', 'POST','HEAD'])
# def my_profile_view(request):
#     profile = Profile.objects.get(user=request.user)
#     form = ProfileModelForm(request.POST, request.FILES or None, instance=profile)
#     serializer = ProfileSerializer(profile, many=False)
    
#     update_flag = False
    
#     if request.method == 'GET':
#         if form.is_valid():
#             form.save()
#             update_flag = True

#     return Response(serializer.data)


@login_required
@api_view(['GET', 'POST','HEAD'])
def received_invites_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False

    if len(results) == 0:
        is_empty = True

    
    context = {'qs': results,
            'is_empty': is_empty,
                }

    return render(request, 'profiles/received_invites.html', context )

# @login_required
# @api_view(['GET', 'POST','HEAD'])
# def received_invites_view(request):
#     profile = Profile.objects.get(user=request.user)
#     qs = Relationship.objects.invitations_received(profile)
#     serializer = ProfileSerializer(profile , many=True)
#     results = list(map(lambda x: x.sender, qs))
#     is_empty = False

#     if len(results) == 0:
#         is_empty = True
  
#     context = {'qs': results,
#             'is_empty': is_empty,
#                 }
    
#     return Response(serializer.data)

@login_required
@api_view(['GET', 'POST','HEAD'])
def accept_invitation(request):
    if request.method =="POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender , receiver=receiver)
        if rel.status == 'send':
            rel.status ='accepted'
            rel.save()
    return redirect('profiles:my-invites-view')


# @login_required
# @api_view(['GET', 'POST','HEAD'])
# def accept_invitation(request):
#     if request.method =="POST":
#         pk = request.POST.get('profile_pk')
#         sender = Profile.objects.get(pk=pk)
#         receiver = Profile.objects.get(user=request.user)
#         serializer = Profile.objects.get(user=request.user)
#         rel = get_object_or_404(Relationship, sender=sender , receiver=receiver)
#         if rel.status == 'send':
#             rel.status ='accepted'
#             rel.save()
#     return Response(serializer.data)
      
    
@login_required
@api_view(['GET', 'POST','HEAD'])
def reject_invitation(request):
    if request.method =="POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender , receiver=receiver)
        rel.delete()   
    return redirect('profiles:my-invites-view')


# @login_required
# @api_view(['GET', 'POST','HEAD'])
# def reject_invitation(request):
#     if request.method =="POST":
#         pk = request.POST.get('profile_pk')
#         sender = Profile.objects.get(pk=pk)
#         receiver = Profile.objects.get(user=request.user)
#         serializer = Profile.objects.get(user=request.user)
#         rel = get_object_or_404(Relationship, sender=sender , receiver=receiver)
#         rel.delete()   
#         #rel.save()
#     return Response(serializer.data)




@login_required
@api_view(['GET', 'POST','HEAD'])
def invite_profiles_list_view(request):
    sender = request.user
    qs = Profile.objects.get_all_profiles_to_invite(sender)
    
    context = {'qs': qs}
    
    return render(request, 'profiles/to_invite_list.html',context)


# @login_required
# @api_view(['GET', 'POST','HEAD'])
# def invite_profiles_list_view(request):
#     sender = request.user
#     qs = Profile.objects.get_all_profiles_to_invite(sender)
#     serializer = request.user
    
#     context = {'qs': qs}
    
#     return Response(serializer.data)



@login_required
@api_view(['GET', 'POST','HEAD'])
def send_invitation(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        rel.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')



# @login_required
# @api_view(['GET', 'POST','HEAD'])
# def send_invitation(request):
#     if request.method=='POST':
#         pk = request.POST.get('profile_pk')
#         user = request.user
#         sender = Profile.objects.get(user=user)
#         receiver = Profile.objects.get(pk=pk)
#         serializer = Profile.objects.get(user=user)
#         rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

#         rel.save()
#         return redirect(request.META.get('HTTP_REFERER'))
#     return Response(serializer.data)


@login_required
@api_view(['GET', 'POST','HEAD'])
def remove_from_friends(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get((Q(sender=sender) & Q(receiver=receiver)) | Q(sender=receiver) & Q(receiver=sender))
        rel.delete()

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('profiles:my-profile-view')

# @login_required
# @api_view(['GET', 'POST','HEAD'])
# def remove_from_friends(request):
#     if request.method=='POST':
#         pk = request.POST.get('profile_pk')
#         user = request.user
#         sender = Profile.objects.get(user=user)
#         receiver = Profile.objects.get(pk=pk)
#         serializer = Profile.objects.get(user=user)

#         rel = Relationship.objects.get((Q(sender=sender) & Q(receiver=receiver)) | Q(sender=receiver) & Q(receiver=sender))
#         rel.delete()

#         return redirect(request.META.get('HTTP_REFERER'))

#     return Response(serializer.data)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name =  'profiles/detail.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile


    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)

        rel_receiver = []
        rel_sender = []

        for item in rel_r:
            rel_receiver.append(item.receiver.user)

        for item in rel_s:
            rel_receiver.append(item.sender.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        #context['is_empty'] = False
        context['posts'] = self.get_object().get_all_author_posts()
        context['no_of_posts'] = True if len(self.get_object().get_all_author_posts()) > 0 else False
        
        return context



class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profiles_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)

        rel_receiver = []
        rel_sender = []

        for item in rel_r:
            rel_receiver.append(item.receiver.user)

        for item in rel_s:
            rel_receiver.append(item.sender.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        #context['profile'] = profile
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context



# class ProfileView(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
