# Using the app

The front page of the app is at [https://fish-catch-forum.herokuapp.com/](https://fish-catch-forum.herokuapp.com/).
It contains a list of all the users currently signed up and the the number of posts they have submitted. The navigation bar
at the top of the view consists of a few different links. To display the main page click `Fish catch forum`. To list all posts click `List posts`. To add a post (login required) click `Add a post`. To create a group (login required) click `Create new group` and to list all groups click `List groups`. To log in with an existing username and password click `Log in`. To sign up click `Sign up`.

### User profile

After signing up you will be automatically logged in. After logging in, your username will be displayed as a link at the top right of the navigation bar. By clicking the link you will be directed to your personal profile page. You can change your password by clicking the `Update password` link. To delete your profile click the `Delete profile` button. This will delete your profile from the database along with all the posts you have added.

### Log out

Click the `Log out` link displayed at the top right of the navigation bar.

## Groups

The navigation bar displays the currently active group. By default this group is the group labelled `Main`. When a user signs up they will automatically be added to the `Main` group. Users cannot leave the `Main` group.

### Listing groups

Click the `List groups` link to list all groups. You have the option of joining or leaving any group created by yourself or other users. By clicking the name of any of the respective groups you will be directed to the posts page for that group. 

### Creating a new group

To add a group click the `Create new group` link on the navigation bar.

## Posts

### Listing posts

Clicking the `List all posts` link on the navigation bar you can view all the posts that have been submitted to the current group.

### Adding a post

To add a post to the current group click the `Add a post` link on the navigation bar. If you are not logged in you will be directed to the log in page.

If you haven't yet joined the group you are trying to add a post to, you will be redirected to the list groups page.

To add a post, fill in the form. The `Species` input takes text input and the `Weight (kg)` takes a decimal number. Add a picture from the file system by clicking the `Choose file` button. Adding a picture is not required. Click the `Add post` button to submit your post.

### Viewing a post

To view a post you must be on the `List all posts` page. View a post by clicking the link next to `Species:`.

### Updating a post

When viewing a post, then if the post was added by you, you can update the post by clicking the `Update` link.

Fill in the parts of the form you want to change. If your post has a picture it will be displayed. Note that when choosing a new picture from the file system, the selected picture will not show up until the `Update post` button has been clicked. 

If you wish to remove the picture from your post then tick the `Tick for no picture` box. The picture will be removed after you click the `Update post` button.

### Deleting a post

When viewing a post, then if the post was added by you, you can delete the post by clicking the `Delete` button.
