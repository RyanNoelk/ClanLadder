## Project Summary:
This project is designed to provide a fun a competitive ranking system for a small subset of players (about 100), for the game StarCraft II. For a complete listing of how points are calculated please see the “How It Works” section.

## Features:
* Replay file parsing.
* Full match history.
* Unique ranking system.

## App List:
1. Accounts – Stores all custom views and templates for user login and password resets. Uses the built in Django user backend to store user information. Contains the views for the admin site.
2. ClanLadder – Core App. This stores all the basic static and html templates as well as the entire server and project configuration.
3. django_ajax – Third party Django Ajax app used to perform all the Ajax operations through the project.
4. Ladder – Stores all the current player information. Contains the main views, templates, and models for the about section and the home page.
5. MatchHistory – Stores all of the history for all of the matches played in every session. Contains the views, templates, and models for match submission, history and player stat views.

## Database Model:
Please see the file Database_UML.png for the database model. 

## Frameworks:
* Django (https://www.djangoproject.com/)
* Bootstrap (http://getbootstrap.com/)
* Datatables (https://datatables.net/)
