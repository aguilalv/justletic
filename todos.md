
# Project to-dos #

## Fixes ##

- [ ] Change first part of keys urls from "users" to "keys"
- [ ] User list and token list API requests need to return a dictionary and not a list (e.g. {"users" : [...]})

## Tech roadmap: High Priority ##

- [ ] Add logging to exchange spotify code for token view
- [ ] Separate Keys.Views.Exchange_Strava_code into exchanging the code and directing to another view that gets and presents the latest activities
- [ ] Update to Python 3.7 and check if there is a newer version of Django
- [ ] Add get token API endpoint for client to acquire its API token (admin and username password to be stored in variables and created at deploy)
- [ ] Eliminate duplication of create user helper and return user
- [ ] Reorganise template architecture to follow best practices
- [ ] Add logging to API (If needed)

## Product roadmap ##

- [ ] Add integration with Runtastic
- [ ] Add sportstracks support
- [ ] Add evaluation across 3 key dimensions on congratulations page and add next step in the journey to ask 'what´s your goal'
- [ ] 'Athlete detail view' (think if best to use request.user to use authenticated user)
- [ ] When input an existing user in Hero Section, check if the user has authorised Strava already and redirect to log-in. If the user has not authorised Strava redirect to Strava authorisation flow
- [ ] Change danger color in bootstrap template to a nicer one
- [ ] Design the error in Strava authorization ux flow and the page

- [ ] Option to commit money that will go to charity if you don't follow the plan (Option for justletic to double that money for charity if you follow the plan but don't achieve your goals)

## Research ##

- [ ] Relational vs non-relational databases to choose one
    - [ ] Consider if it would be better to use relational for core app and non-relational for exercise data, and data analysis
- [ ] How to run periodically python scripts using the webserver (nginx, gunicorn)

## Tech roadmap: Backlog ##

- [ ] Use state parameter in Strava and Spotify oAuth requests to avoid security problems
- [ ] Fix issue with logs functional tests only working when called alone
- [ ] Review that logs generated for all scenarios make sense
- [ ] Research and try to set-up sentry as an error reporting service
    - See [this] (https://lincolnloop.com/blog/disabling-error-emails-django/)
    - and [this] (https://sentry.io/features/) 
- [ ] Write functional tests for all links, buttons, actions ... in the webpage
- [ ] Write functonal tests to test logs work as expected
- [ ] Write functional tests for logs in all important scenarios
- [ ] Consider using warning logging level for failed login and try to include IP address info
- [ ] Add throttling controls to the API 

## At some point ... ##

- [ ] Review layout and styling functional test to make sure it is still adequate andtests the right things 

## Notes ##

https://www.youtube.com/watch?v=CZ3wIuvmHeM - Microservices

coverage run --source=myapp,anotherapp ---omit=*/migrations/* ./manage.py test
coverage run --source='.' manage.py test
coverage report
coverage html
nosetests -v --with-coverage --cover-erase --cover-html

set -a; source .env; set +a

grep -r -l -e TODO  . | grep -e py | grep -v -e cover

ngrok lets you open your localhost server to the internet (good for oauth testing)

python manage.py test
