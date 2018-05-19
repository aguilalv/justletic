[ ] Design the error in Strava authorization ux flow and the page
[ ] Change danger color in bootstrap template to a nicer one
[ ] Support more than 1 service per user
    - There is one URL to authenticate for each service
    - Single view to get service key receives service name from url and stores service name in key model
    - 'Table' of supported services with name and redirect URL (In database? constant?)
[ ] Use django messages instead of passing an error elment in the context
[ ] Think if I need to use request.user inside the 'view detail' view and check that a user is logged in and that it is the same user in the session that the user id to show
[ ] Review layout and styling functional test to make sure it is still adequate andtests the right things 
[ ] It might be worth having separate tests for the authentication backend. Build them - Then use mocks to patch authentication and avoid retesting it in views
[ ] Write functional tests for all links, buttons, actions ... in the webpage

[ ] Add a created field in the user model and initialize with datetime.now() in the create_user method of the user manager
[ ] Research if it is worth using Django Forms instead of nothing

NOTES
=====

coverage run --source=myapp,anotherapp ---omit=*/migrations/* ./manage.py test
coverage run --source='.' manage.py test
coverage report
coverage html
nosetests -v --with-coverage --cover-erase --cover-html

set -a; source .env; set +a

grep -r -l -e TODO  . | grep -e py | grep -v -e cover
