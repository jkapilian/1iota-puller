import requests
import json
import time
import db
from deepdiff import DeepDiff

def main():
	try:
		file = open("shows.json", "r")
		arr = json.loads(file.read())
		file.close()
	except:
		arr = {}
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

							item = db.checkEvent(eventId)

							if (item):
								#item.first
								#if (compare fields) is different:
									#db.updateItem(item, event)
								pass
							else:
								db.putItem(eventId, event)

							break
							#if event is not there, adds event
							#if event is there but is the same as most recent time, does nothing
							#if event is there but is different, adds a new field for cur_time in event

							# if eventId not in arr.keys(): 
							# 	arr[eventId] = {
							# 		cur_time: event
							# 	}
							# 	print(f'New Show: {title} - {event["localStartDay"]} at {event["when"]} in {event["where"]}')
							# else:
							# 	cur_event = arr[eventId][max(arr[eventId].keys())]
							# 	if event != cur_event:
							# 		arr[eventId][cur_time] = event
							# 		print(f'Updated: {title} - {event["localStartDay"]} at {event["when"]} in {event["where"]}')
							# 		print(DeepDiff(cur_event, event))

					break
			except:
				print(f'Issue with {api_route} {id}')
			break
				
		writeFile = open("shows.json", "w")
		writeFile.write(json.dumps(arr))
		writeFile.close()

if __name__ == "__main__":
	# print(db.checkEvent("81134"))
	# db.putItem("",{})
	main()