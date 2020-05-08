# Multi-User-Blog
A basic blog that is maintained by multiple users, with a simple login system.
## Usage
Open the `blog_app.py` file and run it. There's no need to run the `blog_db` file to create the database. 
Once the flask app is running, the URL will open up a **Sign-In** page. As a new user, create an account by clicking on the **Sign-Up**
link and entering credentials there. Once redirected to the **Sign-In** page, enter the credentials created and you'll be logged into the
blog.

## Posting
There are links for navigating the blog on the top-right corner of the web-page. The username of the logged in user also appears there.
Click on the **ADD** link to navigate to the 'Add a post' page. Add the necessary contents for the blog as mentioned here in the page. 
When finished writing for the blog, press **SEND**. This will re-direct you to the home page.

## Navigation
The **HOME** link will show all the blog posts made by all the different users with the latest one being on top. Clicking on any post will
open the complete post. When done posting, you can click on the **SIGNOUT** link to log-out and come back to the login page. You can also
login or sign-up as another user once logged out. If any entry error relevant to credentials occur, a JSON error message will appear with 
the error message and status code. Simply press *Back* on the browser to go back and re-enter the login details accordingly.
