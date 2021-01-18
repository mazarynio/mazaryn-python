from django.db import models
import profiles.models as t
from django.db.models import Q

class RelationshipManager(models.Manager):
    """ This class mimics the functionality of object manager i.e Relationship.objects.filter() --->>
    Relationship.objects.invitations_received()"""
    
    def invitations_received(self, receiver):
        rlnshp_query_set = t.Relationship.objects.filter(receiver=receiver, status='send')
        return rlnshp_query_set
        
accepted_invitations = [] 


class ProfileManager(models.Manager):
    
    def get_all_profiles(self, myself):
        profiles = t.Profile.objects.all().exclude(user=myself)
        return profiles
    
                                             
    
    