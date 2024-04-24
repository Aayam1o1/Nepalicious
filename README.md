# Nepalicious
Nepalicious is a web application designed to provide users with a seamless experience for discovering authentic Nepalese recipes, exploring nearby restaurants, purchasing ingredients, and connecting with fellow food enthusiasts. 



## Features
- **Recipe Blog:** Browse a diverse collection of Nepalese recipes contributed by home cooks and chefs.
- **Restaurant Finder:** Discover Nepalese restaurants near you and explore their menus.
- **Online Marketplace:** Shop for authentic Nepalese ingredients and cooking equipment.
- **User features:** Save your favorite recipes, leave feedback, and connect with other users.
- **Vendor Profile:** Manage products, track orders, and engage with customers.
- **Chef Profile:** Showcase your recipes, interact with users, and build a following.
- **Restaurant Profile:** Make your restaurant online, add restaurant and show location in map.




## Installation

To run the Nepalicious locally, follow these steps:

1. Install Python:

    Install python and python-pip ingby follow the steps from the below reference document based on your Operating System. Reference: https://phoenixnap.com/kb/how-to-install-python-3-windows

2.  Setup virtual environment

    Install Virtual environment
    py -m venv .venv

    Activate the venv
   
        Windows: .\venv\Scripts\activate
        Mac/Linux: source .venv/bin/activate

3.  Clone git repository

        git clone "https://github.com/Aayam1o1/Nepalicious.git"

4.  Install requirements
s
        cd nepalicious/
        pip install -r requirements.txt


5.  Run the migration command

      #### Make migrations
        -python manage.py makemigrations
        -python manage.py migrate

8.  Run the server

    Run the server
    
        python manage.py runserver 8000
      
   # your server is up on port 8000
   # Run this url
       http://127.0.0.1:8000