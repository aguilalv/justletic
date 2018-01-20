Feature: Authorize Strava
    As a non-registered user
    I want to be able to create an account and authorize Justletic to access my Strava data
    So that I can start receiving personalised advice

    Scenario: Create new account and authorize Strava

        When I visit "/"
        Then I will see the title "Justletic"
        And I will see "Justletic" in the header
        And I am invited to type in a text box that says "Enter your email"

        When I type "edith@mailinator.com" into a text box and press enter
        #Then I am redirected to a Strava authorisation page

        #When I authorize Justletic to access my Strava data
        #Then I am redirected back to Justletic
        #And I see a thank you message
        #And I see my last workout was on xxx
