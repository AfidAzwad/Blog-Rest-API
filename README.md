# Blog-Rest-API

Technology:

      ● Database: postgresql
      ● Backend: Django-rest-framework

***--------What we have in this API-----------***



Registration and Login:
      
      ● Used JWT authentication
      ● A non registered user will be able to register
      ● OTP will be sent to email to active a brand new account
      ● Using correct credentials(email & pass) a registered user will be able to log in
      ● User can reset password
      ● Valid user(email) will request for pass reset and an OTP will be sent to user’s email,
      using that OTP new pass will be saved
      ● For OTP maintain User model extended with the fields - [user, otp, has_used, task_type{active_account,
      reset_pass}]


Blog post:

01. Post create:
   
        ● Only registered user will be able to create a post
        ● Only owner of the post have the right to edit or delete that post
        ● Every post have(title, description, status:{published, draft}, created_by, created,
        modified)


2. Display post list:.
   
        ● All the post will be shown in post list page with proper pagination
        ● User without login will be able to see the post
        ● User will be able to apply filter and search keyword to find desire post within the post list


3. Display post details:
   
        ● In the post details user will be able to see a single post with all of its comments
        ● User without login will be able to see the post details + comments


Comments:

      ● A comment will have(comment_by, body, created, modified)
      ● Only a logged in user can create a comment against a post
      ● Owner of a comment can edit and delete that comment
