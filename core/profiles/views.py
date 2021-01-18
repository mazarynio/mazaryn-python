from django.shortcuts import render
from .forms import ProfileModelForm
from .models import Profile, Relationship


# Create your views here.
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    update_flag = False
    
    if request.method == 'POST':
        if form.is_valid:
            form.save()
            update_flag = True
        
    context = {
        'profile': profile,
        'form': form,
        'update_flag': update_flag

    }
    return render(request, 'profiles/myprofile.html', context)


def received_invites_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    
    context = {'qs': qs}
    
    return render(request, 'profiles/received_invites.html', context )
    
    
    
def profiles_list_view(request):
    myself = request.user
    qs = Profile.objects.get_all_profiles(myself)
    
    context = {'qs': qs}
    
    return render(request, 'profiles/profiles_list.html',context)
    

def invite_profiles_list_view(request):
    sender = request.user
    qs = Profile.objects.get_all_profiles_to_invite(sender)
    
    context = {'qs': qs}
    
    return render(request, 'profiles/to_invite_list.html',context)
    
        