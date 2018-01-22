[![Build Status](https://travis-ci.org/TeGie/skrc-link-shortener.svg?branch=master)](https://travis-ci.org/TeGie/skrc-link-shortener)

# Skrc link shortener

Fueled by Django 2.0.1, tested with Selenium, build with Travis, deployed on Heroku.

    # venv
    pip install -r requirements.txt

    # all tests
    python manage.py collectstatic -i admin
    python manage.py test
    
    # for django tests
    python manage.py test analytics/ shorty/
    
    # for selenium tests
    python manage.py test functional_tests/
    
For functional tests you might need Chrome and/or Firefox and Geckodriver: https://github.com/mozilla/geckodriver/releases. 
Download and extract it and put it somewhere on your system path (eg. _/usr/local/bin_ for Linux).