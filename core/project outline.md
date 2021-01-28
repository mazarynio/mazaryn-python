APPS
Pre-requisites are pillow need to be installed , i suppose version django 3...
    profiles
        Profile
            This model currently handles the logic of users profiles has fields ie. first and last names, bio , friends , profile creation date.

            Has methods get_friends, get_friends_no, get_post_no, get_all_author_posts, get_no_of_likes_given, get_no_of_likes_received.
                
                get_friends--->> returns all friends
                get_friends_no--->>counts the number of friends of  the logged in user
                get_post_no----->>counts the number of posts of the logged in user
                get_all_author_posts --->> returns all posts linked to a specific author(ordering method is defined my the class Meta)
                get_no_of_likes_given --->> Returns all likes given to posts by a specific author.
                get_no_of_likes_received --->> Returns all likes linked to posts of a specific author.
            
            All the views are currently function based.

            Signals:post_save_create_profile creates a new profile every time a new user instance is created.

                    post_save_add_friends adds and updates the friends list 

        
        Relationship
            This model currently handles the logic of sender, receiver, relationship status,creation and updated and created date

        ProfileManager and RelationshipManager extends the default Object manager to incoperate the methods  in the model Profile and Relationship

    posts
        Like
            This model currently has the field value etc.

            
        Comment
            This model currently has the field body 
        
        
        Posts
            This model currently has the fields content, image , liked, author,created and updated fields.

            Has methods no_of_likes , no_of_comments.


            Views file has functions post_comment_create_and_list_view displays 'default' post and comment view page

            like_unlike_post handles the logic of liking a post

            classes PostUpdateView and PostDeleteView basically handles best what their name defines ....