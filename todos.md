
# Project to-dos #


## Fixes ##

- [ ] Correct UNIQUE validation error when entering an existing user in hero section
- [ ] Add logging tests and code to accounts.change_password view

## Tech roadmap: High Priority ##

- [ ] Reorganise template architecture to follow best practices

## Product roadmap ##

- [ ] Add evaluation across 3 key dimensions on congratulations page and add next step in the journey to ask 'what´s your goal'
- [ ] 'Athlete detail view' (think if best to use request.user to use authenticated user)
- [ ] Change danger color in bootstrap template to a nicer one
- [ ] Design the error in Strava authorization ux flow and the page
- [ ] Add sportstracks support

## Research ##

- [ ] Relational vs non-relational databases to choose one
- [ ] Using django models from python script
- [ ] Run periodically python scripts using the webserver (nginx, gunicorn)

## Tech roadmap: Backlog ##

- [ ] Review that logs generated for all scenarios make sense
- [ ] Research and try to set-up sentry as an error reporting service
    - See [this] (https://lincolnloop.com/blog/disabling-error-emails-django/)
    - and [this] (https://sentry.io/features/) 
- [ ] Write functional tests for all links, buttons, actions ... in the webpage
- [ ] Write functonal tests to test logs work as expected
- [ ] Write functional tests for logs in all important scenarios
- [ ] Consider using warning logging level for failed login and try to include IP address info

## At some point ... ##

- [ ] Review layout and styling functional test to make sure it is still adequate andtests the right things 

## Notes ##

coverage run --source=myapp,anotherapp ---omit=*/migrations/* ./manage.py test
coverage run --source='.' manage.py test
coverage report
coverage html
nosetests -v --with-coverage --cover-erase --cover-html

set -a; source .env; set +a

grep -r -l -e TODO  . | grep -e py | grep -v -e cover
