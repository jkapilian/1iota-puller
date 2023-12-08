import urllib.request
import json
import csv

def main():
	try:
		file = open("shows.json", "r")
		arr = json.loads(file.read())
		file.close()
	except:
		arr = []
	with urllib.request.urlopen("https://prod-tickets.1iota.com/api/homepage") as response:
		resp_json = json.loads(response.read())
		for section in resp_json["pageSections"]:
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
						if(event["isSoldOut"] == False):
							if event["eventId"] not in arr:
								arr.append(event["eventId"])
								print(f'{title} available on {event["localStartDay"]} at {event["when"]} in {event["where"]}')
		writeFile = open("shows.json", "w")
		writeFile.write(json.dumps(arr))
		writeFile.close()

if __name__ == "__main__":
	main()