# P4-Timeline

## Project description

Timeline, a social media platform designed for users to connect, share, and engage with each other. Whether you want to keep up with your friends, share your latest updates, or discover new people, Timeline provides a streamlined and interactive experience.

[Live Site Link](https://p4-timeline-3238b4375b60.herokuapp.com/)

![Mock up](documentation/all-devices-black.png)

## Table of Contents

- [P4-Timeline](#project-name)
  - [Table of Contents](#table-of-contents)
- [User Experience Design](#user-experience-design)
  - [The Strategy Plane](#the-strategy-plane)
    - [Site Goals](#site-goals)
    - [User Stories](#user-stories)
    - [Agile Planning (Optional)](#agile-planning-optional)
  - [The Scope Plane](#the-scope-plane)
  - [The Structure Plane](#the-structure-plane)
    - [Features](#features)
    - [Features Left to Implement (Optional)](#features-left-to-implement-optional)
  - [The Skeleton Plane](#the-skeleton-plane)
    - [Wireframes](#wireframes)
    - [Database Design](#database-design)
    - [Security](#security)
  - [The Surface Plane](#the-surface-plane)
    - [Design](#design)
    - [Color Scheme](#color-scheme)
    - [Typography](#typography)
    - [Imagery](#imagery)
- [Technologies](#technologies)
- [Testing](#testing)
- [Deployment](#deployment)
  - [Version Control](#version-control)
  - [Deployment Instructions](#deployment-instructions)
  - [Run Locally](#run-locally)
  - [Forking the Project](#forking-the-project)
- [Credits](#credits)

## User Experience Design

## The Strategy Plane

### Site Goals

- The sites goal is to 

### User Stories

![User Stories](documentation/user-story.png)

#### User Story: View Followers

- **As a**: authenticated user
- **I want to**: view a list of my followers
- **So that**: I can see who is following me

- **Acceptance Criteria**:
  1**AC**: A list of followers is displayed, showing each follower's profile picture, username, and a link to their profile.
  2**AC**: If no followers exist, a message is displayed.

---

#### User Story: View Follows

- **As a**: authenticated user
- **I want to**: view a list of users I follow
- **So that**: I can manage the people I am following

- **Acceptance Criteria**:
  1**AC**: A list of followed users is displayed, showing each user's profile picture, username, and a link to their profile.
  2**AC**: If no follows exist, a message is displayed.

---

#### User Story: View User Profile

- **As a**: user
- **I want to**: view a specific user's profile page
- **So that**: I can see their posts and other profile-related information

- **Acceptance Criteria**:
  1**AC**: The profile page shows the user's posts (timeposts), profile picture, and follow/unfollow button.
  2**AC**: I can also see the user's followers and users they follow.

---

#### User Story: Edit/Delete Post on Profile

- **As a**: user
- **I want to**: edit or delete my own posts on my profile
- **So that**: I can update or remove my previous content

- **Acceptance Criteria**:
  1**AC**: I can edit my post using an edit form and delete it through a delete button with a confirmation modal.
  2**AC**: Posts are updated immediately after editing or deletion.

---

#### User Story: Comment on Posts

- **As a**: user
- **I want to**: add, edit, or delete comments on posts
- **So that**: I can engage with other users' content

- **Acceptance Criteria**:
  1**AC**: I can add comments, and edit or delete my own comments using buttons that trigger modals for confirmation.
  2**AC**: Comments show the date they were posted and the user who commented.

---

#### User Story: Like/Dislike Post

- **As a**: authenticated user
- **I want to**: like or dislike a post
- **So that**: I can express my opinion on the content

- **Acceptance Criteria**:
  1**AC**: Clicking like or dislike updates the respective counters.

---

#### User Story: Follow/Unfollow User

- **As a**: authenticated user
- **I want to**: follow or unfollow other users
- **So that**: I can keep up with their posts or stop receiving updates from them

- **Acceptance Criteria**:
  1**AC**: A follow/unfollow button is present on each user's profile, updating immediately after action.
  2**AC**: I can follow/unfollow from the profile or from the list of followers/followed.

---

#### User Story: View All Users

- **As a**: authenticated user
- **I want to**: see a list of all users on the platform
- **So that**: I can explore other user profiles

- **Acceptance Criteria**:
  1**AC**: A list of users is displayed, showing each user's profile picture, username, and a link to their profile.
  2**AC**: If no users are found, a message is displayed.

---

#### User Story: View Timeline

- **As a**: authenticated user
- **I want to**: view a timeline of posts made by other users
- **So that**: I can stay updated on their activities

- **Acceptance Criteria**:
  1**AC**: The timeline displays posts in reverse chronological order.
  2**AC**: Each post includes content, an optional image, like and dislike counts, and a comment button.
  3**AC**: I can see who created the post and when.

---

#### User Story: Create New Post

- **As a**: authenticated user
- **I want to**: create a new post
- **So that**: I can share my thoughts or updates

- **Acceptance Criteria**:
  1**AC**: There is a form where I can type my post and optionally upload an image.
  2**AC**: After submitting, the post appears on the timeline with a timestamp.

---

#### User Story: Edit My Post

- **As a**: user
- **I want to**: edit my own post
- **So that**: I can correct mistakes or update content

- **Acceptance Criteria**:
  1**AC**: I can edit my post by clicking an edit button.
  2**AC**: Changes are saved and updated on the timeline.

---

#### User Story: Delete My Post

- **As a**: user
- **I want to**: delete my post
- **So that**: I can remove it from the timeline

- **Acceptance Criteria**:
  1**AC**: I can delete my post by clicking a delete button with a confirmation prompt.

---

#### User Story: Add Comment to Post

- **As a**: user
- **I want to**: add a comment to a post
- **So that**: I can engage with the content or author

- **Acceptance Criteria**:
  1**AC**: A button opens the comment section for each post.
  2**AC**: I can type and submit a comment, which appears under the post.

---

#### User Story: Edit/Delete Comment

- **As a**: user
- **I want to**: edit or delete my comments on a post
- **So that**: I can correct mistakes or remove comments

- **Acceptance Criteria**:
  1**AC**: I see options to edit or delete my comments.
  2**AC**: The comment updates after editing or is removed after deletion.

---

#### User Story: Search for Users

- **As a**: authenticated user
- **I want to**: search for other users by their username
- **So that**: I can find and view their profile

- **Acceptance Criteria**:
  1**AC**: A search bar allows me to enter a query.
  2**AC**: Results show matching users and link to their profiles.

---

#### User Story: View My Profile

- **As a**: authenticated user
- **I want to**: view my own profile
- **So that**: I can see my posts and activities

- **Acceptance Criteria**:
  1**AC**: A "My Profile" link in the navbar takes me to my profile with my posts and details.

---

#### User Story: View Other Users' Profiles

- **As a**: authenticated user
- **I want to**: view other users' profiles
- **So that**: I can see their posts and activities

- **Acceptance Criteria**:
  1**AC**: Clicking on a user’s name from their posts or comments takes me to their profile page.

---

#### User Story: Logout

- **As a**: authenticated user
- **I want to**: log out of my account
- **So that**: I can leave the session securely

- **Acceptance Criteria**:
  1**AC**: A "Logout" button in the navbar logs me out and redirects to the login page.

---

#### User Story: View Timeline Without Login

- **As a**: unauthenticated user
- **I want to**: see a welcome message prompting me to sign up or log in
- **So that**: I understand I need an account to view the timeline

- **Acceptance Criteria**:
  1**AC**: A welcome message with login and register buttons appears.
  2**AC**: I cannot view the timeline unless logged in.

---

#### User Story: Register

- **As a**: new user
- **I want to**: register for an account
- **So that**: I can start using the platform

- **Acceptance Criteria**:
  1**AC**: A "Register" button in the navbar takes me to the registration page.
  2**AC**: After registration, I am redirected to the homepage and logged in.

---

#### User Story: Login

- **As a**: returning user
- **I want to**: log in to my account
- **So that**: I can access my profile and interact with posts

- **Acceptance Criteria**:
  1**AC**: A "Login" button in the navbar takes me to the login page.
  2**AC**: After logging in, I am redirected to the timeline page.

---

#### User Story: Notifications

- **As a**: user
- **I want to**: see success or error notifications after actions
- **So that**: I know the outcome of my actions

- **Acceptance Criteria**:
  1**AC**: I receive alerts after submitting posts, editing comments, or deleting content.
  2**AC**: Notifications disappear automatically or can be closed manually.

### Agile Planning (Optional)

### User Management

- **Encompasses**:
  - **User Story 1: View Followers**
    - **As a**: authenticated user
    - **I want to**: view a list of my followers
    - **So that**: I can see who is following me
    - **Acceptance Criteria**:
      1. A list of followers is displayed, showing each follower's profile picture, username, and a link to their profile.
      2. If no followers exist, a message is displayed.

  - **User Story 2: View Follows**
    - **As a**: authenticated user
    - **I want to**: view a list of users I follow
    - **So that**: I can manage the people I am following
    - **Acceptance Criteria**:
      1. A list of followed users is displayed, showing each user's profile picture, username, and a link to their profile.
      2. If no follows exist, a message is displayed.

  - **User Story 3: Follow/Unfollow User**
    - **As a**: authenticated user
    - **I want to**: follow or unfollow other users
    - **So that**: I can keep up with their posts or stop receiving updates from them
    - **Acceptance Criteria**:
      1. A follow/unfollow button is present on each user's profile, updating immediately after action.
      2. I can follow/unfollow from the profile or from the list of followers/followed.

  - **User Story 4: Search for Users**
    - **As a**: authenticated user
    - **I want to**: search for other users by their username
    - **So that**: I can find and view their profile
    - **Acceptance Criteria**:
      1. A search bar allows me to enter a query.
      2. Results show matching users and link to their profiles.

  - **User Story 5: View Other Users' Profiles**
    - **As a**: authenticated user
    - **I want to**: view other users' profiles
    - **So that**: I can see their posts and activities
    - **Acceptance Criteria**:
      1. Clicking on a user’s name from their posts or comments takes me to their profile page.

- **Involves**:
  - Displaying user lists and profiles
  - Managing user follow relationships
  - Searching for users and navigating profiles

### Profile Management

- **Encompasses**:
  - **User Story 6: View User Profile**
    - **As a**: user
    - **I want to**: view a specific user's profile page
    - **So that**: I can see their posts and other profile-related information
    - **Acceptance Criteria**:
      1. The profile page shows the user's posts (timeposts), profile picture, and follow/unfollow button.
      2. I can also see the user's followers and users they follow.

  - **User Story 7: View My Profile**
    - **As a**: authenticated user
    - **I want to**: view my own profile
    - **So that**: I can see my posts and activities
    - **Acceptance Criteria**:
      1. A "My Profile" link in the navbar takes me to my profile with my posts and details.

  - **User Story 8: Edit/Delete Post on Profile**
    - **As a**: user
    - **I want to**: edit or delete my own posts on my profile
    - **So that**: I can update or remove my previous content
    - **Acceptance Criteria**:
      1. I can edit my post using an edit form and delete it through a delete button with a confirmation modal.
      2. Posts are updated immediately after editing or deletion.

  - **User Story 9: Edit My Post**
    - **As a**: user
    - **I want to**: edit my own post
    - **So that**: I can correct mistakes or update content
    - **Acceptance Criteria**:
      1. I can edit my post by clicking an edit button.
      2. Changes are saved and updated on the timeline.

  - **User Story 10: Delete My Post**
    - **As a**: user
    - **I want to**: delete my post
    - **So that**: I can remove it from the timeline
    - **Acceptance Criteria**:
      1. I can delete my post by clicking a delete button with a confirmation prompt.

- **Involves**:
  - Viewing and managing profiles and posts
  - Editing and deleting personal content

### Post Interaction

- **Encompasses**:
  - **User Story 11: Comment on Posts**
    - **As a**: user
    - **I want to**: add, edit, or delete comments on posts
    - **So that**: I can engage with other users' content
    - **Acceptance Criteria**:
      1. I can add comments, and edit or delete my own comments using buttons that trigger modals for confirmation.
      2. Comments show the date they were posted and the user who commented.

  - **User Story 12: Like/Dislike Post**
    - **As a**: authenticated user
    - **I want to**: like or dislike a post
    - **So that**: I can express my opinion on the content
    - **Acceptance Criteria**:
      1. Clicking like or dislike updates the respective counters.

  - **User Story 13: Add Comment to Post**
    - **As a**: user
    - **I want to**: add a comment to a post
    - **So that**: I can engage with the content or author
    - **Acceptance Criteria**:
      1. A button opens the comment section for each post.
      2. I can type and submit a comment, which appears under the post.

  - **User Story 14: Edit/Delete Comment**
    - **As a**: user
    - **I want to**: edit or delete my comments on a post
    - **So that**: I can correct mistakes or remove comments
    - **Acceptance Criteria**:
      1. I see options to edit or delete my comments.
      2. The comment updates after editing or is removed after deletion.

- **Involves**:
  - Interacting with posts through comments and reactions
  - Managing comments on posts

### Content Management

- **Encompasses**:
  - **User Story 15: Create New Post**
    - **As a**: authenticated user
    - **I want to**: create a new post
    - **So that**: I can share my thoughts or updates
    - **Acceptance Criteria**:
      1. There is a form where I can type my post and optionally upload an image.
      2. After submitting, the post appears on the timeline with a timestamp.

  - **User Story 16: Edit My Post**
    - **As a**: user
    - **I want to**: edit my own post
    - **So that**: I can correct mistakes or update content
    - **Acceptance Criteria**:
      1. I can edit my post by clicking an edit button.
      2. Changes are saved and updated on the timeline.

- **Involves**:
  - Creating and updating posts on the platform

### Timeline Management

- **Encompasses**:
  - **User Story 17: View Timeline**
    - **As a**: authenticated user
    - **I want to**: view a timeline of posts made by other users
    - **So that**: I can stay updated on their activities
    - **Acceptance Criteria**:
      1. The timeline displays posts in reverse chronological order.
      2. Each post includes content, an optional image, like and dislike counts, and a comment button.
      3. I can see who created the post and when.

  - **User Story 18: View Timeline Without Login**
    - **As a**: unauthenticated user
    - **I want to**: see a welcome message prompting me to sign up or log in
    - **So that**: I understand I need an account to view the timeline
    - **Acceptance Criteria**:
      1. A welcome message with login and register buttons appears.
      2. I cannot view the timeline unless logged in.

- **Involves**:
  - Displaying posts on a timeline for logged-in and unauthenticated users

### Authentication and Authorization

- **Encompasses**:
  - **User Story 19: Register**
    - **As a**: new user
    - **I want to**: register for an account
    - **So that**: I can start using the platform
    - **Acceptance Criteria**:
      1. A "Register" button in the navbar takes me to the registration page.
      2. After registration, I am redirected to the homepage and logged in.

  - **User Story 20: Login**
    - **As a**: returning user
    - **I want to**: log in to my account
    - **So that**: I can access my profile and interact with posts
    - **Acceptance Criteria**:
      1. A "Login" button in the navbar takes me to the login page.
      2. After logging in, I am redirected to the timeline page.

  - **User Story 21: Logout**
    - **As a**: authenticated user
    - **I want to**: log out of my account
    - **So that**: I can leave the session securely
    - **Acceptance Criteria**:
      1. A "Logout" button in the navbar logs me out and redirects to the login page.

- **Involves**:
  - User registration, login, and logout processes

### Notifications

- **Encompasses**:
  - **User Story 22: Notifications**
    - **As a**: user
    - **I want to**: see success or error notifications after actions
    - **So that**: I know the outcome of my actions
    - **Acceptance Criteria**:
      1. I receive alerts after submitting posts, editing comments, or deleting content.
      2. Notifications disappear automatically or can be closed manually.

- **Involves**:
  - Providing feedback to users on their actions and system status

These stories involve:
-Backend functionality for administrators to control various aspects of the Timeline operations and user data

### Why These are Epics

- **Complexity**: They involve multiple interconnected features and functionalities, likely requiring more development effort than a single user story.
- **Scope**: They represent broader user goals rather than specific, isolated actions.

