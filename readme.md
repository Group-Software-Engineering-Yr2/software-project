# Ecomon

## Group Team Beep

-   Adam O'Neill
-   Lorenzo Meixieira
-   Callum Ward
-   Jake Mcallister
-   Boris Cheung
-   Angelo Thind
-   Finay Fordham

# Useful Links

## Process Documents

https://trello.com/b/wzoUYlVk/group-software-project

We have taken regular snapshots of the kanban board in trello to archive our progress. `/kanban_screenshots` directory

Within process documents we have also included the meeting notes, agenda and minutes. **todo insert the dir**

## Technical Documents

Our technical documents are primarily managed on the github system. https://github.com/Group-Software-Engineering-Yr2/software-project

Other technical docs are in **todo insert dir**

## PRODUCT DOCUMENTS

The UI and design documents for the client have also been archived in **todo insert dir**

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
