[ ] Get the real key from each service using OAuth2 - Start with Strava

[ ] Change danger color in bootstrap template to a nicer one
[ ] Support more than 1 service per user
    - There is one URL to authenticate for each service
    - Single view to get service key receives service name from url and stores service name in key model
    - 'Table' of supported services with name and redirect URL (In database? constant?)
[ ] Review functional test for multiple users (Currently passing even with keys from different user)
[ ] Use django messages instead of passing an error elment in the context
[ ] Think if I need to use request.user inside the 'view detail' view and check that a user is logged in and that it is the same user in the session that the user id to show

[ ] Reserch if it would be good to run tests and coverage report on a pre-commit hook (research on is jenkins or similar better than a pre-commit hook)
[ ] Review layout and styling functional test to make sure it is still adequate andtests the right things 

NOTES
=====

coverage run --source=myapp,anotherapp ---omit=*/migrations/* ./manage.py test
coverage run --source='.' manage.py test
coverage report
coverage html
nosetests -v --with-coverage --cover-erase --cover-html
