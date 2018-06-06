
# Project to-dos #

## Research ##

- [ ] Relational vs non-relational databases to choose one
- [ ] Using django models from python script
- [ ] Run periodically python scripts using the webserver (nginx, gunicorn)

## Fixes ##

- [ ] Correct UNIQUE validation error when entering an existing user in hero section

## Tech roadmap ##

- [ ] Add logging to Justletic code
    - Use JSON logging
    - Try to write logs asynchronously with a buffer or queue so the app can keep running
    - Log useful information encoded (e.g.
        {"message" : "User clicked on a button",
         "userId" : "1234",
         "buttonId": "save",
         "pageId" : "sign-up"
        }
    - Use logger configuration to structure the info
    - Application should output to the console. Where to store logs is a deployment concern, not an application concern
- [ ] Research and try to set-up sentry as an error reporting service
    - See [this] (https://lincolnloop.com/blog/disabling-error-emails-django/)
    - and [this] (https://sentry.io/features/) 
- [ ] Write functional tests for all links, buttons, actions ... in the webpage

## Product roadmap ##

- [ ] 'Athlete detail view' (think if best to use request.user to use authenticated user)
- [ ] Change danger color in bootstrap template to a nicer one
- [ ] Design the error in Strava authorization ux flow and the page
- [ ] Design key journeys and pages
- [ ] Add sportstracks support

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
