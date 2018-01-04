Feature: Authorize Strava
    As a non-registered user
    I want to be able to create an account and authorize Justletic to access my Strava data
    So that I can start receiving personalised advice

    Scenario: Create new account and authorize Strava

        When I visit "/"
        Then I will see the title "Justletic"
