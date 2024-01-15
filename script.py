import urllib.request
import json
import time

def main():
	try:
		file = open("shows.json", "r")
		arr = json.loads(file.read())
		file.close()
	except:
		arr = {}
	with urllib.request.urlopen("https://prod-tickets.1iota.com/api/homepage") as response:
		resp_json = json.loads(response.read())
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
					with urllib.request.urlopen(f"https://prod-tickets.1iota.com/api/{api_route}/{id}") as show_response:
						show_json = json.loads(show_response.read())
						for event in show_json[resp_key]:
							eventId = str(event["eventId"])
							if eventId not in arr.keys():
								arr[eventId] = {
									cur_time: event
								}
								print(f'New Show: {title} - {event["localStartDay"]} at {event["when"]} in {event["where"]}')
							elif event != arr[eventId][max(arr[eventId].keys())]:
								arr[eventId] = {
									cur_time: event
								}
								print(f'Updated: {title} - {event["localStartDay"]} at {event["when"]} in {event["where"]}')
			except:
				print(f'Issue with {api_route} {id}')
				
		writeFile = open("shows.json", "w")
		writeFile.write(json.dumps(arr))
		writeFile.close()

if __name__ == "__main__":
	main()