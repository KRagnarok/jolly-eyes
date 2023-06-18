# Jolly Eyes
The name of the repository was inspired by the toy story movie(Jolly chimp character).

## Goal of the project
The goal of the project is to provide some basic functionalities, such as fetching and filtering emails, to communicate with and get information from different sources 
that use different protocols. Thus, this project will help to get some basic information about unread emails or search the inbox for specific emails by using APIs.

## Usage
Create a new file named **config.json** that has same structure as it is shown in the **config_ex.json**. Fill the necessary information, such as username and password, then place your 
communication protocol, currently IMAP and Exchange are supported, after that, you can run the app.

## Note
This project is a service for another project named **Toru**.

## Remaining Tasks(In the long run)

- [ ] Design an API that allows to get content of an email
- [ ] Support 'AND' and 'OR' logic for filters
- [ ] Reuse the same connection in order to fetch data from servers
- [ ] Design an API that allows to add emails
- [ ] Add more protocols, such as Pop3
- [ ] Support additional settings, such as routing a specific email through proxy or vpn
- [ ] Add an authentication method to APIs
- [ ] Add better error handling mechanisms
