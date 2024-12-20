# **Welcome to the SNB Banking Application!** #  

## **Important** ##
Please make sure when running the application that the 'customer_records.json' file and the 'accounts.json' file are located in the same root folder as the 'SNB_banking_application.py' file.  

Both the JSON files must not be left completely empty for the program to function correctly. If you wish to erase all customer records and account data then please keep an empty dictionary or list in both of these JSON files.  

## Testing ##
Three test accounts have been created for ease of testing, each with two current, two savings, and two mortgage accounts.

To access these accounts please refer to their customer logins below:
* (Username: customer_one - Password: 1) 
* (Username: customer_two - Password: 2) 
* (Username: customer_three - Password: 3)  

The admin login is:
* (Username: admin - Password: access)  

## Side Note ##
Floating point numbers were not used to represent currency because of the rounding errors they produce. Instead pounds and pence are represented as seperate integers which are then correctly formated together when required.