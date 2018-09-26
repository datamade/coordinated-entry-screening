# Coordinated Entry Screening (CES)

The Coordinated Entry Screening tool helps people experiencing homelessness in Chicago and its surrounding suburbs. The tool guides users through a series of questions to determine eligibility for [Coordinated Entry Access points](https://www.csh.org/chicagoces/) and other resources. Users can complete the survey via text-message or on a web interface. 

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

`rapidsms-decision-tree` app requires a database for storing information about [messages, answers, and tree states](https://github.com/datamade/rapidsms-decisiontree-app/blob/master/decisiontree/models.py). Create your database.

```bash
createdb coordinated-entry-screening
```

Then, run migrations.

```bash
python manage.py migrate
```

Create an admin user. Set a username and password when prompted.

```bash
python manage.py createsuperuser
```

*DataMakers with staging server access!* You can use the web interface (i.e., the `/surveys/` endpoint – see below) to create whatever survey data you like. However, to get started with development, consider dumping the CES staging database and restoring it on your local machine. [Follow this tutorial.](https://github.com/datamade/tutorials/blob/master/Dump-and-restore-Postgres.md) Note! If you use this option, you must first drop your database. 

## Run the tool

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

