import requests, json
from datetime import datetime

def get_upcoming_events(params):
    try:
        endpoint_url = "https://fortinet.my.workfront.com/attask/api/v15.0/task/search"
        response = requests.get(endpoint_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
       
        res_data = json.loads(response.content)["data"]
        events = [{'name': x["name"], "id": x["ID"], "date": x["plannedCompletionDate"]} for x in res_data]        
        
        return events

    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return None


def get_event_assignee_id(events, params):
    try:
        endpoint_url = "https://fortinet.my.workfront.com/attask/api/v15.0/"
        
        for event in events:
            response = requests.get(endpoint_url + "task/" + event["id"], params=params)
            response.raise_for_status()  # Raise an exception for bad status codes

            res_data = json.loads(response.content)["data"]
            event["assignedToID"]=res_data["assignedToID"]

        return events

    except requests.exceptions.RequestException as e:
       print(f"Error making the request: {e}")
       return None

def get_event_assignee_names(events, params):
    try:
        endpoint_url = "https://fortinet.my.workfront.com/attask/api/v15.0/"
        
        for event in events:
            response = requests.get(endpoint_url + "user/" + event["assignedToID"], params=params)
            response.raise_for_status()  # Raise an exception for bad status codes

            res_data = json.loads(response.content)["data"]
            event["assignedToName"]=res_data["name"]

        return events

    except requests.exceptions.RequestException as e:
       print(f"Error making the request: {e}")
       return None

def main():

    api_key = ""
    project_id = ""

    # Get list of calendar events
    events = get_upcoming_events({'apiKey': api_key, 'projectID': project_id})

    # Get IDs of task assignees
    events_w_assignees = get_event_assignee_id(events, {'apiKey': api_key, 'fields': 'assignedToID'})

    # Replace assignee IDs with names
    events_assignee_names = get_event_assignee_names(events_w_assignees, {'apiKey': api_key,})

    # date formatting
    date_fmt = '%Y-%m-%dT%H:%M:%S:%f%z'

    print("Upcoming events: ")
    for x in events_assignee_names:
        x_date=datetime.strptime(x["date"], date_fmt)
        print(x["name"]+","+x["assignedToName"]+","+str(x_date.month)+"/"+str(x_date.day)+"/"+str(x_date.year))

if __name__ == "__main__":
    main()
