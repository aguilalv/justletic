
FIXES
=====

TECH ROADMAP
============

[ ] Change to standard authentication library ... or ...
[ ] It might be worth having separate tests for the authentication backend. Build them - Then use mocks to patch authentication and avoid retesting it in views
[ ] Add a created field in the user model and initialize with datetime.now() in the create_user method of the user manager
[ ] Add logging to Justletic code
    - Use JSON logging
    - Try to write logs asynchronously with a buffer or queue so the app can keep running
    - Log useful information encoded (e.g.
        {"message" : "User clicked on a button",
         "userId" : "1234",
         "buttonId": "save",
         "pageId" : "sign-up"
        }
    - Use logger configuration to structure the info
[ ] Think if I need to use request.user inside the 'view detail' view and check that a user is logged in and that it is the same user in the session that the user id to show
[ ] Research if it is worth using Django Forms instead of nothing
[ ] Write functional tests for all links, buttons, actions ... in the webpage

PRODUCT ROADMAP
===============

[ ] Change danger color in bootstrap template to a nicer one
[ ] Design the error in Strava authorization ux flow and the page

AT SOME POINT
=============

[ ] Review layout and styling functional test to make sure it is still adequate andtests the right things 

NOTES
=====

coverage run --source=myapp,anotherapp ---omit=*/migrations/* ./manage.py test
coverage run --source='.' manage.py test
coverage report
coverage html
nosetests -v --with-coverage --cover-erase --cover-html

set -a; source .env; set +a

grep -r -l -e TODO  . | grep -e py | grep -v -e cover

url = "https://www.strava.com/api/v3/athlete/activities"
headers = {'Authorization': 'Bearer 245756813830c8e24116ce778dfabf2c827a079e'}
r = requests.get(url,headers=headers)
