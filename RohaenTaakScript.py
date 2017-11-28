#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
import json
import copy

baseLine = {
	"Complexity": 0.0,
	"Minutes": 15120.0,
}

auth = ("", "")

boardId = "522"

base = {
	"fields": {
		"project":
		{
			"key": "FRGDXL"
		},
		#"customfield_10301": "1261", #sprint to create the issue under
		"summary": "test description",
		"description": "",
		"issuetype": {
			"name": "Task"
		},
		"priority": {
			"name": "Major"
		},
		"timetracking":
		{
			"originalEstimate": "",
			"remainingEstimate": ""
		}
	}
}

def formatDescription(issue):
	return "Detailed: {}\n\nPreconditions: {}\n\nPostConditions: {}\n\nNeeded resources: {}".format(issue["Detailed"], issue["Preconditions"], issue["PostConditions"], issue["NeededResources"])

def mapIssue(issue, issueType, parent = None):
	timeEstimate = int((baseLine["Minutes"] / baseLine["Complexity"]) * issue["Complexity"])
	data = copy.deepcopy(base)

	if issueType == "Epic":
		data["fields"]["customfield_10401"] = issue["EpicName"]

	if parent != None:
		if issueType == "Sub-task":
			data["fields"]["parent"] = { "key": parent }
		elif issueType == "Task":
			data["fields"]["customfield_10400"] = parent

	data["fields"]["issuetype"]["name"] = issueType
	data["fields"]["summary"] = issue["Summary"]
	data["fields"]["description"] = formatDescription(issue)
	data["fields"]["timetracking"]["originalEstimate"] = str(timeEstimate) + "m"
	data["fields"]["timetracking"]["remainingEstimate"] = str(timeEstimate) + "m"
	return data

def createIssue(issue):
	print issue
	result = requests.post("http://jira.icaprojecten.nl/rest/api/2/issue/", auth = auth, json = issue)
	if result.status_code < 200 or result.status_code >= 300:
		print result.status_code
		print result.text
		raise Exception('A very specific bad thing happened')

	print result

	return result.json()["key"]


def writeToCsv(stuff):
	csv = open("workfile","w") 
	for epic in stuff:
		csv.write("epic: " + epic["Summary"] + "\n")
		for story in epic["Children"]:
			csv.write("Task: " + story["Summary"] + "\n")
			for task in story["Children"]:
				csv.write("Sub-task: " + task["Summary"] + "\n")
	csv.close()

def createGraph(stuff):
	for epic in stuff:
		graph = open(epic["EpicName"] + ".plantuml","w") 
		for story in epic["Children"]:
			graph.write("rectangle \"" + story["Summary"] + "\" {\n")
			i = 0
			firstWord = story["Summary"].split(' ', 1)[0]
			for task in story["Children"]:
				i = i + 1
				graph.write("  (" + task["Summary"] + ") as " + firstWord + str(i) + "\n")
			graph.write("}\n")
		graph.close()

def createIssues(stuff):
	for epic in stuff:
		data = mapIssue(epic, "Epic")
		if epic["Id"] is None:
			epic["Id"] = createIssue(data)

		for story in epic["Children"]:
			data = mapIssue(story, "Task", epic["Id"])
			if story["Id"] is None:
				story["Id"] = createIssue(data)

			for task in story["Children"]:
				data = mapIssue(task, "Sub-task", story["Id"])
				if task["Id"] is None:
					task["Id"] = createIssue(data)

def getSprints(boardId):
	result = requests.get("http://jira.icaprojecten.nl/rest/agile/1.0/board/" + boardId + "/sprint", auth = auth)
	if result.status_code < 200 or result.status_code >= 300:
		print result.status_code
		print result.text
		raise Exception('A very specific bad thing happened')

	return result.json()

def sanityCheck(stuff):
	for epic in stuff:
		mapIssue(epic, "Epic")
		for story in epic["Children"]:
			mapIssue(story, "Task", epic["Id"])
			for task in story["Children"]:
				mapIssue(task, "Sub-task", story["Id"])


issues = [
	{
		"Id": None,
		"EpicName": "Vision",
		"Summary": "Dit zijn alle taken voor het vision groepje",
		"Detailed": "Een groep die zich focussed op het herkennen van een beker met opencv.",
		"Preconditions": "Er zijn webcams beschikbaar.",
		"PostConditions": "Een module waarmee bekers herkent kunnen worden.",
		"NeededResources": "Webcam",
		"Priority": "Major",
		"Complexity": 0,
		"Children": [
			{
				"Id": None,
				"Summary": "",
				"Detailed": "",
				"Preconditions": "",
				"PostConditions": "",
				"NeededResources": "",
				"Priority": "Major",
				"Complexity": 0,
				"Children": [
					{
						"Id": None,
						"Summary": "",
						"Detailed": "",
						"Preconditions": "",
						"PostConditions": "",
						"NeededResources": "",
						"Priority": "Major",
						"Complexity": 0
					},
					{
						"Id": None,
						"Summary": "",
						"Detailed": "",
						"Preconditions": "",
						"PostConditions": "",
						"NeededResources": "",
						"Priority": "Major",
						"Complexity": 0
					}
				]
			}
		]
	}, {
		"Id": None,
		"EpicName": "UI",
		"Summary": "UI groep",
		"Detailed": "Dit zijn de taken die benodigd zijn om de UI te realiseren.",
		"Preconditions": "",
		"PostConditions": "",
		"NeededResources": "",
		"Priority": "Major",
		"Complexity": 0,
		"Children": [
			{
				"Id": None,
				"Summary": "",
				"Detailed": "",
				"Preconditions": "",
				"PostConditions": "",
				"NeededResources": "",
				"Priority": "Major",
				"Complexity": 0,
				"Children": [
					{
						"Id": None,
						"Summary": "",
						"Detailed": "",
						"Preconditions": "",
						"PostConditions": "",
						"NeededResources": "",
						"Priority": "Major",
						"Complexity": 0
					},
					{
						"Id": None,
						"Summary": "",
						"Detailed": "",
						"Preconditions": "",
						"PostConditions": "",
						"NeededResources": "",
						"Priority": "Major",
						"Complexity": 0
					}
				]
			}
		]
	},
	{
		"Id": None,
		"EpicName": "Kinematica & planning",
		"Summary": "Kinemetica & planning groep",
		"Detailed": "Dit zijn alle taken die vallen onder het groepje kinematica & planning. Dit groepje is verantwoordelijk voor de robotarm aansturing.",
		"Preconditions": "",
		"PostConditions": "",
		"NeededResources": "",
		"Priority": "Major",
		"Complexity": 0,
		"Children": [
			{
				"Id": None,
				"Summary": "Inverse kinematics implementeren",
				"Detailed": "",
				"Preconditions": "",
				"PostConditions": "",
				"NeededResources": "",
				"Priority": "Major",
				"Complexity": 0,
				"Children": [
					{
						"Id": None,
						"Summary": "",
						"Detailed": "",
						"Preconditions": "",
						"PostConditions": "",
						"NeededResources": "",
						"Priority": "Major",
						"Complexity": 0
					},
					{
						"Id": None,
						"Summary": "",
						"Detailed": "",
						"Preconditions": "",
						"PostConditions": "",
						"NeededResources": "",
						"Priority": "Major",
						"Complexity": 0
					}
				]
			}
		]
	},
	{
		"Id": None,
		"EpicName": "Gezamelijk",
		"Summary": "Gezamelijke taken",
		"Detailed": "Dit zijn de gezamelijke taken die niet onder een van de deelgroepjes vallen.",
		"Preconditions": "",
		"PostConditions": "",
		"NeededResources": "",
		"Priority": "Major",
		"Complexity": 0,
		"Children": [
			{
				"Id": None,
				"Summary": "SAD bijwerken",
				"Detailed": "Het SAD moet bijgewerkt worden met de huidige staat.",
				"Preconditions": "SAD komt niet overeen met huidige situatie",
				"PostConditions": "SAD komt overeen met de huidige situatie",
				"NeededResources": "",
				"Priority": "Major",
				"Complexity": 0,
				"Children": [
					{
						"Id": None,
						"Summary": "Hoofstuk een + twee controleren en uitbreiden",
						"Detailed": "De eerste twee hoofdstukken moeten gecontroleerd en uitgebreid worden",
						"Preconditions": "",
						"PostConditions": "Eerste en tweede hoofdstukken komen overeen met implementatie",
						"NeededResources": "",
						"Priority": "Major",
						"Complexity": 4
					},
					{
						"Id": None,
						"Summary": "Omschrijven van lagen model naar component diagram en lagen model laten staan.",
						"Detailed": "Joost heeft ons sterk aangeraden het lagen model ook in een component model te zetten. SDD architectural overview moet hier ook bijgewerkt worden.",
						"Preconditions": "",
						"PostConditions": "Component model volgens lagen model staat in het SAD.",
						"NeededResources": "",
						"Priority": "Major",
						"Complexity": 3
					},
					{
						"Id": None,
						"Summary": "Deelsystemen updaten",
						"Detailed": "De deelsystemen moeten in lijn zijn met de implementatie. SDD architectural overview moet hier ook bijgewerkt worden.",
						"Preconditions": "",
						"PostConditions": "Deelsystemen zijn in lijn met de implementatie.",
						"NeededResources": "",
						"Priority": "Major",
						"Complexity": 1
					},
					{
						"Id": None,
						"Summary": "Use case realization updaten",
						"Detailed": "Use case realization met kloppen met de deelsystemen en er moet duidelijk gemaakt worden dat dit een high level view is en niet direct overeenkomt met functie calls.",
						"Preconditions": "",
						"PostConditions": "Sequence diagram klopt met implementatie en er is expliciet aangegeven dat het om high-level view gaat.",
						"NeededResources": "",
						"Priority": "Major",
						"Complexity": 3
					},
					{
						"Id": None,
						"Summary": "Package- lagen structuur en gebruik van frameworks updaten.",
						"Detailed": "Package- lagen structuur en gebruik van frameworks moet bijgewerkt worden. SDD architectural overview moet hier ook bijgewerkt worden.",
						"Preconditions": "",
						"PostConditions": "Package- lagen structuur en gebruik van frameworks moet bijgewerkt zijn en kloppen met implementatie.",
						"NeededResources": "",
						"Priority": "Major",
						"Complexity": 5
					},
					{
						"Id": None,
						"Summary": "Deployment diagram hoofdstuk + subhoofdstukken updaten.",
						"Detailed": "Het deployment diagram komt niet overeen met de implementatie en de huidige architectuur dat moet gefixed worden. Namen van de interfaces moeten erbij. SDD architectural overview moet hier ook bijgewerkt worden.",
						"Preconditions": "",
						"PostConditions": "Deployment diagram klopt met implementatie.",
						"NeededResources": "",
						"Priority": "Major",
						"Complexity": 3
					}
				]
			}
		]
	}, {
		"Id": None, 
		"EpicName": "Point Cloud", 
		"Summary": "Point Cloud", 
		"Detailed": "Een groep die de cloud points realiseert.", 
		"Preconditions": "Kinect en LiDAR zijn beschikbaar.", 
		"PostConditions": "Een module die de objecten in de waarneembare wereld om zich heen beschikbaar stelt.", 
		"NeededResources": "Kinect en LiDAR", 
		"Priority": "Major", 
		"Complexity": 0, 
		"Children": [
			{
				"Id": None,
				"Summary": "",
				"Detailed": "",
				"Preconditions": "",
				"PostConditions": "",
				"NeededResources": "",
				"Priority": "Major",
				"Complexity": 0,
				"Children": [
					{
						"Id": None,
						"Summary": "",
						"Detailed": "",
						"Preconditions": "",
						"PostConditions": "",
						"NeededResources": "",
						"Priority": "Major",
						"Complexity": 0
					},
					{
						"Id": None,
						"Summary": "",
						"Detailed": "",
						"Preconditions": "",
						"PostConditions": "",
						"NeededResources": "",
						"Priority": "Major",
						"Complexity": 0
					}
				]
			}
		]
	}
]


baseLine["Complexity"] = sum([subTask["Complexity"] for epic in issues for task in epic["Children"] for subTask in task["Children"]])

print baseLine
sanityCheck(issues)
createGraph(issues)
#createIssues(issues)

writeToCsv(issues)

#createIssues(issues)