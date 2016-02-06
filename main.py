#!/usr/bin/python
import requests
import json
import os
from datetime import datetime
from twilio.rest import TwilioRestClient

def open_config(mode):
    cwd = os.getcwd()
    if 'sms-commit-activity' in cwd:
        cwd = ''
    else:
        cwd = cwd + '/sms-commit-activity/'

    config_file = open(cwd+'config.json', mode)
    return config_file

def get_config():
    config = json.load( open_config('r') )
    return config

def update_config(id):
    config_file = open_config('r')
    data = json.load(config_file)
    config_file.close()

    data['github']['last_event_id'] = id

    config_file = open_config('w')
    config_file.write(json.dumps(data, sort_keys=True, indent=4))
    config_file.close()

def get_events(username):
    events = requests.get("https://api.github.com/repos/%s/events?per_page=5" % username)
    events = json.loads(events.text)
    return events

def check_commit_activity(github):
    events = get_events(github['org_repo'])
    last_event_id = github['last_event_id']
    new_events = []
    index = 0
    event_id = events[index]['id']
    update_config(event_id)
    while event_id != last_event_id:
        username = events[index]['actor']['login']
        commits = events[index]['payload']['commits']
        for commit in commits:
            commit_msg = commit['message']
            new_events.append( "'" + commit_msg + "' -> " + username + "," )

        index += 1
        event_id = events[index]['id']

    return list( reversed(new_events) )

def send_sms(twilio, events):
    client = TwilioRestClient( twilio['sid'], twilio['auth_token'] )

    message_body = str( len(events) ) + " new " + ('commit' if len(events) ==1 else 'commits') + ": \r\n"
    message_body += ' \r\n'.join(events)
    message = client.messages.create(
        to = twilio["number_to"],
        from_ = twilio["number_from"],
        body = message_body
    )

def main():
    config = get_config()
    events = check_commit_activity(config['github'])
    if events:
        send_sms(config['twilio'], events)

if __name__ == "__main__":
    main()
