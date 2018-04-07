[ ] Get the real key from each service using OAuth2 - Start with Strava
[ ] Change danger color in bootstrap template to a nicer one
[ ] Support more than 1 service per user
    - There is one URL to authenticate for each service
    - Single view to get service key receives service name from url and stores service name in key model
    - 'Table' of supported services with name and redirect URL (In database? constant?)
[ ] Review functional test for multiple users (Currently passing even with keys from different user)
[ ] Use constants instead of hardcoded strings for errors (both in tests and code)
[ ] Install and configure PyLint and hook it to check code quality im every commit
[ ]Install coverage. Then to run it: coverage run --source='.' manage.py test myapp
and then coverage report
[ ] Use django messages instead of passing an error elment in the context
[ ] Think if I need to use request.user inside the 'view detail' view and check that a user is logged in and that it is the same user in the session that the user id to show