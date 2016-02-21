# sms-commit-activity
Receive SMS notifications for commits to a repository

> Main idea behind this project is to track an organization or personal repository and get updates for changes done by your team!


## Requirements

### Installing Python dependencies
```python
pip install -r requirements.txt
```
### Twilio Account
Signup for a [Twilio](https://www.twilio.com) account

### Server / VM
A server is required to run script as a cronjob so that script will run continuously as long as server is running.


## Setting Up The Server

### Build The Script
```bash
cd ~
git clone https://github.com/codenirvana/sms-commit-activity.git
cd sms-commit-activity
pip install -r requirements.txt
crontab -e
```

Using ```crontab -e``` setup a new cronjob.
example:
```bash
# Run every 1 hour
0 */1 * * * ~/sms-commit-activity/main.py

# Run every 10 minutes
*/10 * * * * ~/sms-commit-activity/main.py
```

**NOTE:**
* ```sms-commit-activity``` folder must be placed at your home ```~``` directory.
* While testing this script on your PC, you can place the ```sms-commit-activity``` folder in any directory.


## Configurations
Open config.json file and fill relevant information.

**org_repo** : your_org_username/your_repo_name

**last_event_id** : Open this [https://api.github.com/repos/{org_repo}/events](https://api.github.com/repos/{org_repo}/events) link  and change *org_repo* with your_org_username/your_repo_name
Copy the first ```id: xxxxxxxxxx``` and replace with *ID* in config file.

**twilio**
From your twilio account get the ACCOUNT SID, AUTH TOKEN and Generated Number.
*Only verified numbers will work in number_to*

TODO
====
- [ ] Track Multiple Repos


##Licence
Open sourced under [MIT License](LICENSE)
