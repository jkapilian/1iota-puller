import requests
import json
import time
import db
import sns
from deepdiff import DeepDiff

def main():
	try:
		file = open("shows.json", "r")
		arr = json.loads(file.read())
		file.close()
	except:
		arr = {}
	message_str = "New 1iota changes:\n\n"
	changed = ""
	with requests.get("https://prod-tickets.1iota.com/api/homepage") as response:
		resp_json = response.json()
		cur_time = time.time()
		for section in resp_json["pageSections"]:
			try:
				for show in section["items"]:
					title = show["altText"]
					path_arr = show["path"].split("/")
					celeb = path_arr[0] == "fanbase"
					id = path_arr[2] if celeb else path_arr[1]
					api_route = "celeb" if celeb else "project"
					resp_key = "eventList" if celeb else "events"
					with requests.get(f"https://prod-tickets.1iota.com/api/{api_route}/{id}") as show_response:
						show_json = show_response.json()
						for event in show_json[resp_key]:
							eventId = str(event["eventId"])

							cur_event = db.checkEvent(eventId)

							if (cur_event is None):
								print("here")
								db.putItem(eventId, event, cur_time)
								changed += (f'New Show: {title} - {event["localStartDay"]} at {event["when"]} in {event["where"]}')
							else:
								if event != cur_event:
									db.putItem(eventId, event, cur_time)
									changed += (f'Updated: {title} - {event["localStartDay"]} at {event["when"]} in {event["where"]}\n')
									changed += (f'{DeepDiff(cur_event, event)}\n\n')
								
			except:
				print(f'Issue with {api_route} {id}')

		if changed != "":
			sns.publish(message_str + changed)

		writeFile = open("shows.json", "w")
		writeFile.write(json.dumps(arr))
		writeFile.close()

if __name__ == "__main__":
	main()
