# CS50W-Commerce
### Commerce is a Django which allows users to buy and sell items through auctions.
It is part of the <a href="https://cs50.harvard.edu/web/2020/">CS50’s Web Programming with Python and JavaScript course.</a><br>
The project requirements can be found <a href = "https://cs50.harvard.edu/web/2020/projects/2/commerce/">here.</a>
<img width="960" alt="image" src="https://user-images.githubusercontent.com/102196421/162672014-a8c3a726-92f2-4b22-97d1-6e7e3ac73da7.png">
<img width="960" alt="image" src="https://user-images.githubusercontent.com/102196421/162671993-70424318-2da5-4069-8601-c87053e9e980.png">
<img width="960" alt="image" src="https://user-images.githubusercontent.com/102196421/162672092-29f86cf1-86ab-4d34-9237-76618cc56041.png">
<img width="960" alt="image" src="https://user-images.githubusercontent.com/102196421/162672140-6c015065-2357-416e-a23b-676cd1c94c04.png">
# Getting Started
## Requirements
You must have <a href="https://code.visualstudio.com/docs/python/python-tutorial">Python</a> and <a href="https://www.djangoproject.com/download/">Django</a> installed in your vscode<br>
## Download or pull the code
`git clone https://github.com/eduymil/CS50W-Commerce.git`
## Download required dependencies
`pip install Pillow`<br>
## Make Migrations
1. `cd` into the commerce directory
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
## Create admin account
1. Run `python manage.py createsuperuser`
2. Enter your desired username and password
3. Admin rights can accessed through the /admin route in the url
## Run Program
1. Ensure that you are in the right directory (`cd` into commerce):
2. Execute `python manage.py runserver` in your terminal
