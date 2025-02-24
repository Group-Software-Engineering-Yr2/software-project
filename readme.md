# Software Project
# Software Project

# Useful Links

https://trello.com/b/wzoUYlVk/group-software-project

# Project

Project located in /technical-documents/source-code/ecomon

## Installation

All requirements are serialized in requirements.txt

`pip install -r requirements.txt`

## Running the server

Ensure the database is fully migrated

`python3 manage.py migrate`

Then run the local development server

`pyhton3 manage.py runserver`

and navigate [here](http://localhost:8000/) to begin

## Custom Commands

Resetting all the gyms to their default state:

`python3 manage.py reset_gyms`

Requires the fossil fuel arbitrary user to be set up. username = fossil_fuels

## CronTab

Ensure cron jobs are added. May need to run twice:

`python3 manage.py crontab add`

To run cron jobs locallyL

`python3 manage.py crontab run {id}`

# License

# Members

-   Adam O'Neill
-   Lorenzo Meixieira
-   Callum Ward
-   Jake Mcallister
-   Boris Cheung
-   Angelo Thind
-   Finay Fordham

# License

# Members

-   Adam O'Neill
-   Lorenzo Meixieira
-   Callum Ward
-   Jake Mcallister
-   Boris Cheung
-   Angelo Thind
-   Finay Fordham
