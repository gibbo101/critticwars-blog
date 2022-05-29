# Manual Testing
* [Manual Testing](#manual-testing)
  * [Bugs and Fixes During the Development Process]
  (#bugs-and-fixes-during-the-development-process)
* [Lighthouse](#lighthouse)



## Bugs and Fixes During the Development Process
Below is a list of bugs and fixes found whilst creating the project. Most are listed on the [GitHub Projects Board(https://github.com/gibbo101/critticwars-blog/projects/2)]
As bugs were discovered through the sprint a card was made to then fix it.

### Issue: Heroku Deployment
* Cause: When deploying to Heroku I was getting an error. Upon looking at the logs, there was an error with backports, which was being put in the requirements.tx file when running pip3 freeze --local > rrequirements.txt
* Fix: Removed backports from the requirements.txt file.

### Issue: Blog posts not showing in a list
* Cause: Called incorrect blog variable 
    {% for Blog in blog_list %}
    <p>{{ blog.title }}, {{ blog.author }}</p>
* Fix: changed Blog to blog

### Issue: Add comment form not working
* Cause: Incorrect use of form tags.
* Fix: form action="post" set to form method="post"

### Issue: Likes not working
* Cause: Incorrect arguments called
* Fix: Added *args, **kwargs to method

### Issue: Account Signup link not working
* Cause: Incorrect URL path being called
* Fix: Call correct url path of 'account_signup'

### Issue: Cloudinary not serving static files on Heroku
* Cause: Unknown. After some research I still couldn't determine why Cloudinary wasn't working
* Fix: Switched to whitenoise to serve static files

### Issue: Whitnoise not working correctly
* Cause: Incorrect configuration in middleware and installed apps in settings.py
* Fix: Set whitenoise configuration to the correct order in the middlewaree and apps lists

### Issue: Account registration causing errors
* Cause: Nothing configured to send confirmation emails in django
* Fix: ACCOUNT_EMAIL_VERIFICATION = 'none' in settings.py to disable verification emails

 ### Issue: Updated table not recognised on Heroku
* Cause: Adding to database models and then testing mistakenly on Heorku rather than the local server. I then made some migrations in an attempt to roll back the database but ended up breaking local environment as well and could not restore db table to fix. 
* Fix: Hard reset of git repository to the night before and a fake roll back of db migrations to then re-run old migrations to fix.

### Issue: When deleting a user their comments don't delete
* Cause: Comments table not linked to Users
* Fix: Add a ForeignKey row into the Comments table and cascade on delete

### Issue: Creating the CwUsers table and showing name in the comments
* Cause: Unable to hook into Comments and compare names
* Fix: Set ForeignKey in CwUsers to reference User and Comments table. In views.py got all CwUser instances and allowed accass in the html file where I then looped whilst in the comments loop. If names didnt match or cw_id was not 0 then it displays CritticWars character name and ID.

### Issue: On delete account page, back button was also deleting account(and without safety alert)
* Cause: Button tag was within form tags.
* Fix: Set button type="button" and this stopped it submiting within the form tags.

### Issue: Pagination for comments broke comments count and CritticWars charactger names showing
* Cause: paginator takes comments in views.py a value to determine pagination causing comments in the template to show as "Page 1 of 1"
* Fix: set a new variable of new_comments = comments before pagination called and use this to determine number of comments and rename cw_comments to cw_users in template. 


### Issue: Flash messages showing underneath nav bar
* Cause: Setting nav bar to be fixed to the top of the screen.
* Fix: Move flash messages into the main tag and set margins to push content below the nav bar

# Lighthouse
The lighthouse test showed a reduced score for accessibility as the nav bar had 2 drop down items. The error was "duplicate id elements." I fixed this by changing the id to a class. 

## Blog List
### Desktop
![Blog List Desktop Score](docs/images/lighthouse/blog-list-desktop.png)
### Mobile
![Blog List Mobile Score](docs/images/lighthouse/blog-list-mobile.png)

## Blog Post and Comments
### Desktop
* Initial score for Best Practice was 83 due to using a low res image. This has now been resolved.
![Blog Post Desktop Score](docs/images/lighthouse/blog-post-desktop.png)
### Mobile
![Blog Post Mobile Score](docs/images/lighthouse/blog-post-mobile.png)

## User Settings
### Desktop
![User Settings Desktop Score](docs/images/lighthouse/user-settings-desktop.png)
### Mobile
![User Settings Mobile Score](docs/images/lighthouse/user-settings-mobile.png)

## Delete Account
### Desktop
![Delete Account Desktop Score](docs/images/lighthouse/delete-account-desktop.png)
### Mobile
![Delete Account Mobile Score](docs/images/lighthouse/delete-account-mobile.png)

## Edit Comments
### Desktop
![Edit Comments Desktop Score](docs/images/lighthouse/edit-comments-desktop.png)
### Mobile
![Edit Comments Mobile Score](docs/images/lighthouse/edit-comments-mobile.png)

## Delete Comments
### Desktop
![Delete Comments Desktop Score](docs/images/lighthouse/delete-comments-desktop.png)
### Mobile
![Delete Comments Mobile Score](docs/images/lighthouse/delete-comments-mobile.png)

## Log Out
### Desktop
![Logout Desktop Score](docs/images/lighthouse/logout-desktop.png)
### Mobile
![Logout Mobile Score](docs/images/lighthouse/logout-mobile.png)

## Login
### Desktop
![Login Desktop Score](docs/images/lighthouse/register-desktop.png)
### Mobile
![Login Mobile Score](docs/images/lighthouse/register-mobile.png)

# Validators
## [HTML](https://validator.w3.org):

Pages were free from errors, except those noted below.

* An error was thrown for using a div tag as a child of a h5 tag on the blog post comments page and the edit and delete comments pages. These have now been fixed.
* There was also an error for no alt tag in an image but this was from a blog post input where I had no control over the image being posted. 
![blog list error](docs/images/validators/html-blog-comments.png)

* Otherwise the site was free of errors.

![html validator](docs/images/validators/html-blog-list.png)

## [CSS](https://jigsaw.w3.org/css-validator/):
My CSS file was tested and found to be free from errors

![html validator](docs/images/validators/css.png)

## [JS](https://jshint.com/):
No errors were found using JShint. 

## [PEP8](http://pep8online.com):
The following errors were found when running through the pep8 checker. 
* devblog/admin.py - 	missing whitespace after ','
* devblog/models.py - line too long, too many blank lines, expected 2 blank lines, found 1
* devblog/urls.py - line too long
* critticwars/settings.py - line too long