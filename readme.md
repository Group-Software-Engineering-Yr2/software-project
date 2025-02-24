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

Within the process documents directory we have also included our Sprint 1 Documentation and Sprint 1 Reflection documents found in `/process-documents` 

We have taken regular snapshots of the kanban board in trello to archive our progress. `/kanban_screenshots` directory

Within process documents we have also included the meeting notes, agenda and minutes. `/meeting-notes`

## Technical Documents

Our technical documents are primarily managed on the github system. https://github.com/Group-Software-Engineering-Yr2/software-project

Requirements txt file is located in `/technical-documents/source-code`

Other technical docs are in `/technical-documents` which include the readme for endpoints and bin_process as well as out github repository screenshot.

## PRODUCT DOCUMENTS

The design documents, requirement analysis and UI for the client have also been archived in: 
<br> `/product-documents/designs` 
<br> `/product-documents/requirement-analysis` 
<br> `/product-documents/ui` respectively.

Our Ecomon slides for the presentation, poster and GDPR can also be found in `/product-documents`

# Project

Project located in `/technical-documents/source-code/ecomon`

Once in the above directory, follow the guide below to run Ecomon!

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
