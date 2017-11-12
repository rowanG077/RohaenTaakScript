#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
import json
import copy

baseLine = {
	"Complexity": 0.0,
	"Minutes": 21600.0,
}

auth = ("username", "password")

boardId = "522"

base = {
	"fields": {
		"project":
		{
			"key": "FRGDXL"
		},
		"customfield_10301": "1261", #sprint to create the issue under
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

def createIssue(issue, issueType, parent = None):
	if issue["Id"] != None:
		return issue["Id"];

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

	result = requests.post("http://jira.icaprojecten.nl/rest/api/2/issue/", auth = auth, json = data)
	if result.status_code < 200 or result.status_code >= 300:
		print result.status_code
		print result.text
		raise Exception('A very specific bad thing happened')

	print issueType + ", id: " + result.json()["key"] + ", " + issue["Summary"]

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

def createIssues(stuff):
	for epic in stuff:
		epic["Id"] = createIssue(epic, "Epic")

		for story in epic["Children"]:
			story["Id"] = createIssue(story, "Task", epic["Id"])

			for task in story["Children"]:
				task["Id"] = createIssue(task, "Sub-task", story["Id"])

def getSprints(boardId):
	result = requests.get("http://jira.icaprojecten.nl/rest/agile/1.0/board/" + boardId + "/sprint", auth = auth)
	if result.status_code < 200 or result.status_code >= 300:
		print result.status_code
		print result.text
		raise Exception('A very specific bad thing happened')

	return result.json()


issues = [
	{
		"Id": None,
		"EpicName": "Some epic name",
		"Summary": "Foo epic",
		"Detailed": "Detailed description for this epic",
		"Preconditions": "Ultimate programmer skills",
		"PostConditions": "Ultimate UML skills",
		"NeededResources": "Internet",
		"Priority": "Major",
		"Complexity": 0,
		"Children": [{
			"Id": None,
			"Summary": "some task",
			"Detailed": "",
			"Preconditions": "",
			"PostConditions": "",
			"NeededResources": "",
			"Priority": "Major",
			"Complexity": 0,
			"Children": [{
				"Id": None,
				"Summary": "Some small task to handle",
				"Detailed": "",
				"Preconditions": "",
				"PostConditions": "",
				"NeededResources": "",
				"Priority": "Major",
				"Complexity": 10
			},{
				"Id": None,
				"Summary": "some small task to handle 2",
				"Detailed": "",
				"Preconditions": "",
				"PostConditions": "",
				"NeededResources": "",
				"Priority": "Major",
				"Complexity": 40
			}]
		}]
	}
]


baseLine["Complexity"] = sum([subTask["Complexity"] for epic in issues for task in epic["Children"] for subTask in task["Children"]])

print baseLine

#createIssues(issues)