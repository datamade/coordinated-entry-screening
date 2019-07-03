# Coordinated Entry Screening (CES)

The Coordinated Entry Screening tool helps people experiencing homelessness in Chicago and its surrounding suburbs. The tool guides users through a series of questions to determine eligibility for [Coordinated Entry Access points](https://www.csh.org/chicagoces/) and other resources. Users can complete the survey via text-message or on a web interface. 

Built in collaboration with the [Corporation for Supportive Housing](https://www.csh.org/).

## Setup

### Dependencies

The Coordinated Entry Screening tool leverages the power of RapidSMS [(a framework built on top of Django for creating mobile services)](https://www.rapidsms.org/), `rapidsms-decisiontree-app` [(an app to support the creation of surveys)](https://rapidsms-decisiontree-app.readthedocs.io/en/latest/), and the [Twilio API](https://www.twilio.com/) for text messaging. DataMade forked, updated, and customized some of these dependencies. At the very least, clone the DataMade fork of `rapidsms-decisiontree-app` to your local machine.

#### DataMade forks

* [rapidsms](https://github.com/datamade/rapidsms) - uses Django 1.11
* [rapidsms-decisiontree-app](https://github.com/datamade/rapidsms-decisiontree-app) - uses Django 1.11 and Python 3, and customized to suit the needs of CES
* [rapidsms-twilio](https://github.com/datamade/rapidsms-twilio), an integration app – uses Twilio 6.16.2

#### Other dependencies 

* [twilio-python](https://github.com/twilio/twilio-python)
* [ngrok](https://ngrok.com/) (*for local development only*)

### Getting started

**Step 1. Create a Twilio trial account and phone number** 

*Note! You might not be developing the text-messaging aspect of this tool. If so, you can skip Step 1 and leave blank `ACCOUNT_SID`, `AUTH_TOKEN`, and `TWILIO_NUMBER` in the settings file (Step 3).**

Visit [twilio.com](https://www.twilio.com/), and follow the steps to signup for a new account. Please note! Trial accounts do not expire, but they can [reach a limit](https://github.com/datamade/coordinated-entry-screening/issues/31) on the number of messages sent. 

Use the Twilio dashboard to add a phone number. Then, add your personal cell phone as a [verified caller](https://support.twilio.com/hc/en-us/articles/223180048-Adding-a-Verified-Phone-Number-or-Caller-ID-with-Twilio), since [trial accounts](https://support.twilio.com/hc/en-us/articles/223136107) only communicate with verified numbers.

**Step 2. Setup a virtualenv, clone the CES repo, and install dependencies.**

We recommend using [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html) for working in a virtualized development environment. [Read how to set up virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Once you have virtualenvwrapper set up, do the following:

```bash
git clone git@github.com:datamade/coordinated-entry-screening.git
cd coordinated-entry-screening
mkvirtualenv coordinated-entry-screening
pip install -r requirements.txt
```

Afterwards, whenever you want to use this virtual environment, run `workon coordinated-entry-screening`.

**Step 3. Create a settings file**

```bash
cp coordinated-entry-screening/settings_deployment.py.example coordinated-entry-screening/settings_deployment.py
```

Update your secret key, and assign values to the Twilio-specific variables (found in your Twilio dashboard).

```bash
SECRET_KEY = 'super secret key of your choosing'

# Look for these on https://www.twilio.com/console
ACCOUNT_SID = '*******************************'
AUTH_TOKEN = '*******************************'

# The number you created above!
TWILIO_NUMBER = '(312) 624-6268'
```

**Step 4. Setup the database**

`rapidsms-decision-tree` app requires a database for storing information about [messages, answers, and tree states](https://github.com/datamade/rapidsms-decisiontree-app/blob/master/decisiontree/models.py). 

The `data` directory has a dump of the database used at the time of launching. It is in custom archive format: you can restore it locally by running the following. [(Read more about dumping and restoring databases.)](https://github.com/datamade/how-to/blob/master/postgres/Dump-and-restore-Postgres.md) 

```bash
pg_restore -C -j4 --no-owner data/ces_launch.dump | psql
```

Create an admin user. Set a username and password when prompted.

```bash
python manage.py createsuperuser
```

Note! To restore the database on the server, do the following.

```bash
ssh ubuntu@connectmenow.org

# drop and create a fresh database
dropdb -U postgres coordinated-entry-screening
createdb -U postgres coordinated-entry-screening

# retore the database
pg_restore -U postgres -C -j4 --no-owner --role=datamade /home/datamade/coordinated-entry-screening-d-<deployment-id>/data/ces_launch.dump | psql -U postgres

# change its owner
psql -U postgres
ALTER DATABASE "coordinated-entry-screening" OWNER TO datamade;
```

If you need to restore the database on the server, after the time of launch, then be sure to preserve the user data in the relevant tables. See the dashboard view for more info.

## Run the tool 

#### Text-messaging 

Phew! Congrats on surviving a massive setup. You are nearly ready to run the tool locally. But first, Twilio needs to know about your local version of the CES tool. To make your app reachable, use Ngrok as advised by [the Twilio docs](https://www.twilio.com/docs/sms/quickstart/python#allow-twilio-to-talk-to-your-flask-application). As the docs describe, you will need two terminal windows: one with Ngrok running, the other with CES.

```bash
# in one window
./ngrok http 8000

# in another
python manage.py runserver
```

Now, visit Twilio and [find the details about your newly created phone number](https://www.twilio.com/console/phone-numbers/incoming). Under "Messaging," add `http://******.ngrok.io/backend/twilio/`
 as a webhook. The exact URL should correspond with whatever Ngrok spits out in your local terminal. 

 The big moment! Send a message to the phone number. The CES trigger word depends on the details of your survey, but for testing purposes, just try "ping." Did the app "pong"?


#### Web interface

This should be a breeze. Just run, and visit the URL provided in your terminal:

```
python manage.py runserver
```

## Data

#### The survey

DataMade and the Corporation for Supportive Housing devised question logic to guide users to resources. The basic survey includes these questions:

* Where are you located?
* What is your age?
* Where did you sleep last night?
* Do you have a child or children?
* Do you have an income, but require short term financial support to help with housing costs, e.g. rent, electric or heating bills, etc.? **(ONLY for 2019)**
* If you slept in the home of a friend or family member or your own home, is it a stable safe place to stay for the forseeable future?
* If you slept in the home of a friend or family member or your own home, are you attempting to flee because it is an unsafe setting? 

Decision trees located in the `data/survey_diagrams` folder visualize how users move from question-to-resource-to-question. We created these using (a free trial of) [LucidChart](https://www.lucidchart.com).

#### Trigger codes

The database has three basic versions of the survey: 

1. a survey for people in the city or suburbs (accessed with the keyword "connect"),
2. a survey for people in the city (accessed with a code, e.g., by texting "0006"),
3. a survey for people in the suburbs (currently, not in use, but may be in the future). 

We populated the database with location-specific trigger codes using an very simple ETL process. CSH provided us with an Excel document with 90+ city codes, and our `Makefile` ported these codes to the database. This process does not need to be repeated, but it can be, if CSH provides a different spreadsheet in the future. 

See the `data` directory for relevant files. 

## Team

* [Regina Compton](https://github.com/reginafcompton)
* [Forest Gregg](https://github.com/fgregg)
* [Jasmine Mithani](https://github.com/jmithani)

## Errors and bugs

Is something not behaving intuitively? [Report it by creating an issue.](https://github.com/datamade/coordinated-entry-screening/issues)

Use [Mozilla's guidelines for reporting bugs](https://developer.mozilla.org/en-US/docs/Mozilla/QA/Bug_writing_guidelines#General_Outline_of_a_Bug_Report) to precisely and concisely describe your issue.

## Patches and pull requests

We welcome your patches! Our suggested workflow:
 
* Fork the project.
* Make your feature addition or bug fix.
* Send us a pull request with a description of your work. 

## Copyright and attribution

Copyright (c) 2018 DataMade. Released under the [MIT License](https://github.com/datamade/coordinated-entry-screening/blob/master/LICENSE).

