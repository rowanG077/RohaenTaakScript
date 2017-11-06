import requests
import json
import copy

baseLine = {
	"Complexity": 261.00,
	"Minutes": 7680.0,
}

auth = ("name", "pw")

base = {
	"fields": {
	   "project":
	   { 
		  "key": "projectName"
	   },
	   "summary": "test desciption",
	   "description": "",
	   "issuetype": {
		  "name": "Task"
	   },
	   "timetracking":
		{
		   "originalEstimate": "",
		   "remainingEstimate": ""
		}
   }
}


def createIssue(summary, description, complexity, issueType, parent = None):
	timeEstimate = int((baseLine["Minutes"] / baseLine["Complexity"]) * complexity)
	data = copy.deepcopy(base)
	if parent != None and issueType == "Sub-task":
		data["fields"]["parent"] = {
			"id": parent
		}

	data["fields"]["issuetype"]["name"] = issueType
	data["fields"]["summary"] = summary
	data["fields"]["description"] = description
	data["fields"]["timetracking"]["originalEstimate"] = str(timeEstimate) + "m"
	data["fields"]["timetracking"]["remainingEstimate"] = str(timeEstimate) + "m"

	print json.dumps(data)

	result = requests.post("http://jira.icaprojecten.nl/rest/api/2/issue/", auth = auth, json = data)
	if result.status_code < 200 or result.status_code >= 300:
		print result.status_code
		print result.text
		raise Exception('A very specific bad thing happened')

	createdId = result.json()["id"]

	if parent != None and issueType == "Task":
		data = {
			"type": {
				"name": "Relates"
			},
			"inwardIssue": {
				"id": createdId
			},
			"outwardIssue": {
				"id": parent
			},
			"comment": {
				"body": "User story link",
			}
		}
		result = requests.post("http://jira.icaprojecten.nl//rest/api/2/issueLink", auth=("rb.goemans@student.han.nl", "1991-11-28"), json = data)
		if result.status_code < 200 or result.status_code >= 300:
			print result.status_code
			print result.text
			raise Exception('A very specific bad thing happened')

	return createdId

stories = [
	{
		"Id": None,
		"Summary": "Uitvoeren expirement",
		"Description": "",
		"Complexity": 0,
		"Tasks": [
			{
				"Id": None,
				"Summary": "SRS opstellen.",
				"Description": "",
				"Complexity": 0,
				"SubTask": [
					{
						"Id": None,
						"Summary": "Introductie schrijven.",
						"Description": "",
						"Complexity": 3
					},
					{
						"Id": None,
						"Summary": "Domain model opstellen.",
						"Description": "",
						"Complexity": 3
					},
					{
						"Id": None,
						"Summary": "Use case diagram maken.",
						"Description": "",
						"Complexity": 3
					},
					{
						"Id": None,
						"Summary": "fully dressed use case.",
						"Description": "",
						"Complexity": 5
					},
					{
						"Id": None,
						"Summary": "System sequence diagram opstellen.",
						"Description": "",
						"Complexity": 8
					},
					{
						"Id": None,
						"Summary": "Operation contracts opstellen.",
						"Description": "",
						"Complexity": 5
					},
					{
						"Id": None,
						"Summary": "Functionele en niet functionele requirements opstellen.",
						"Description": "",
						"Complexity": 5
					}
				]
			},
			{
				"Id": None,
				"Summary": "Onderzoek naar Discrete event simulation.",
				"Description": "",
				"Complexity": 0,
				"SubTask": [
					{
						"Id": None,
						"Summary": "Opstellen Hoofd- en deelvragen.",
						"Description": "",
						"Complexity": 5
					},
					{
						"Id": None,
						"Summary": "Deelvragen uitwerken.",
						"Description": "",
						"Complexity": 13
					},
					{
						"Id": None,
						"Summary": "Inleiding en conclusie schrijven.",
						"Description": "",
						"Complexity": 5
					}
				]
			},
			{
				"Id": None,
				"Summary": "SDD opstellen.",
				"Description": "",
				"Complexity": 0,
				"SubTask": [
					{
						"Id": None,
						"Summary": "Architectuur plaatje maken.",
						"Description": "",
						"Complexity": 5
					},
					{
						"Id": None,
						"Summary": "Deployment diagram maken.",
						"Description": "",
						"Complexity": 8
					},
					{
						"Id": None,
						"Summary": "TLCP protocol design.",
						"Description": "",
						"Complexity": 8
					},
					{
						"Id": None,
						"Summary": "Logging formaat maken.",
						"Description": "",
						"Complexity": 5
					},
					{
						"Id": None,
						"Summary": "Configuratie parameters design maken.",
						"Description": "",
						"Complexity": 8
					},
					{
						"Id": None,
						"Summary": "Simulator UML.",
						"Description": "",
						"Complexity": 13
					},
					{
						"Id": None,
						"Summary": "Simulator design decisions in kaart brengen en verantwoorden.",
						"Description": "",
						"Complexity": 8
					},
					{
						"Id": None,
						"Summary": "Scheduler UML.",
						"Description": "",
						"Complexity": 8
					},
					{
						"Id": None,
						"Summary": "Scheduler design decisions in kaart brengen en verantwoorden.",
						"Description": "",
						"Complexity": 5
					}
				]
			},
			{
				"Id": None,
				"Summary": "Implementeren Scheduler component.",
				"Description": "",
				"Complexity": 0,
				"SubTask": [
					{
						"Id": None,
						"Summary": "Opstellen project met git, jenkins en sonarcube.",
						"Description": "",
						"Complexity": 5
					},
					{
						"Id": None,
						"Summary": "Round robin scheduling Implementeren.",
						"Description": "",
						"Complexity": 8
					},
					{
						"Id": None,
						"Summary": "TLCP protocol integreren.",
						"Description": "",
						"Complexity": 8
					},
					{
						"Id": None,
						"Summary": "Logging implementeren.",
						"Description": "",
						"Complexity": 5
					}
				]
			},
			{
				"Id": None,
				"Summary": "Implementeren Simulatie component.",
				"Description": "",
				"Complexity": 0,
				"SubTask": [
					{
						"Id": None,
						"Summary": "Opstellen project met git, jenkins en sonarcube",
						"Description": "",
						"Complexity": 5
					},
					{
						"Id": None,
						"Summary": "Genereren autos volgens normaalverdeling rond spitsen.",
						"Description": "",
						"Complexity": 13
					},
					{
						"Id": None,
						"Summary": "Implementeren stoplichten en rijbanen.",
						"Description": "",
						"Complexity": 8
					},
					{
						"Id": None,
						"Summary": "Implementeren wegrijden en aankomen autos.",
						"Description": "",
						"Complexity": 13
					},
					{
						"Id": None,
						"Summary": "Implementeren configuratie mogelijkheid.",
						"Description": "",
						"Complexity": 8
					}
				]
			},
			{
				"Id": None,
				"Summary": "Implementeren TLCP protocol en netwerk communicatie.",
				"Description": "",
				"Complexity": 0,
				"SubTask": [
					{
						"Id": None,
						"Summary": "Implementeren TLCP commands.",
						"Description": "",
						"Complexity": 8
					},
					{
						"Id": None,
						"Summary": "Parseren en serializen van TLCP commands uit/naar strings.",
						"Description": "",
						"Complexity": 8
					},
					{
						"Id": None,
						"Summary": "Implementeren server die TLCP commands ontvangt en verstuurd.",
						"Description": "",
						"Complexity": 8
					}
					,
					{
						"Id": None,
						"Summary": "Implementeren client die TLCP commands ontvangt en verstuurd.",
						"Description": "",
						"Complexity": 8
					}
				]
			},
			{
				"Id": None,
				"Summary": "Acceptance testen.",
				"Description": "",
				"Complexity": 0,
				"SubTask": [
					{
						"Id": None,
						"Summary": "Testplan schrijven.",
						"Description": "",
						"Complexity": 20
					},
					{
						"Id": None,
						"Summary": "Testplan uitvoeren.",
						"Description": "",
						"Complexity": 13
					}
				]
			}
		]
	}
]

for story in stories:
	if story["Id"] == None:
		story["Id"] = createIssue(story["Summary"], story["Description"], story["Complexity"], "Story")
	
	for task in story["Tasks"]:
		if task["Id"] == None:
			task["Id"] = createIssue(task["Summary"], task["Description"], task["Complexity"], "Task", story["Id"])
		
		for subTasks in task["SubTask"]:
			subTasks["Id"] = createIssue(subTasks["Summary"], subTasks["Description"], subTasks["Complexity"], "Sub-task", task["Id"])
