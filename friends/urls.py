



path('friends/', FriendsListView.as_view(), name='friends'),
    #     path('myprofile/my-invites/', ReceivedInvitesList.as_view()),
    #     path('myprofile/to-invite/', InvitesProfileList.as_view()),
    path('send_request/<slug:slug>/', send_friend_request, name='send-request'),
    path('accept_request/<slug:slug>/',
         accept_friend_request, name='accept-request'),
    path('myprofile/followers/', FollowersListView.as_view(), name='followers'),
    path('myprofile/following/', FollowingListView.as_view(), name='following'),
    path('all_profiles/follower_add/', follower_add, name='add_follower'),
    path('all_profiles/follower_remove/',
         follower_remove, name='remove_follower'),
        path('myprofile/blocked/', BlockedListView.as_view(), name='blocked'),
    path('myprofile/blocking/', BlockingListView.as_view(), name='blocking'),
    path('myprofile/blocking/block/', block_add, name='block_add'),
    path('myprofile/blocked/unblock/',
         block_remove, name='remove_block'),
    