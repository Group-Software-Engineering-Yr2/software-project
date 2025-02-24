# Bin Setup Process

The bin feature is integral to playing ecomon. Users find bins and recycle their packs while battling against the current bin owner to capture that bin

## Requirements

Team Fossil Fuels are greedy and want to capture all the bins. At the start of every day they come in a steal back all the bins. There must be a user with the username `fossil_fuel` to capture these gyms. This is hard coded requirement from the custom command `python3 manage.py reset_gyms`

To create this user please sign up using the regular sign up screen with the username as specified. If it already exists, it is already setup!

To ensure the daily capture can occur ensure django-crontab is set up correctly. Mentioned in the Readme.md

## Creating Bins

1. Login to the admin pannel (/admin) with a staff account
2. Navigate to Gyms (backend name for bins)
3. Here please add a Bin as required
4. View the created Bin and locate the id
5. Create a QR code `https://[host]/gym-battle/[gym_id]
6. Scan the qr code within the required radius of the longitude and latitude of the bin point to battle the bin

## Battling Bins

Ensure you're within the require radius of the center point of the bin. Then scan the QR code and battle the bin!
