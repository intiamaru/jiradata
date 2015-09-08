import json
import urllib2, base64
import time

#https://yellowpepper.atlassian.net/rest/api/2/search?jql=assignee=amherrera

request = urllib2.Request("https://yellowpepper.atlassian.net/rest/api/2/search?startIndex=0&jql=project=SW&sprint=2&maxResults=1001")
base64string = base64.encodestring('%s:%s' % ('jboneu', 'seekjust1ce')).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)

#capture JSON
result = urllib2.urlopen(request).read()
obj = json.loads(result)

#build custom JSON
data = {}
data = obj["issues"]
json_refactor = []

openIssues = 0
inProgressIssues = 0
resolvedIssues = 0
closedIssues = 0
doneIssues = 0
doneLocallyIssues = 0
reopenedIssues = 0
totalIssues = 0

for position in data:
    dictObject = {}
    dictObject["id"] = position["id"]
    dictObject["key"] = position["key"]
    dictObject["url"] = position["self"]
    
    
    data2 = position["fields"]["assignee"]
    
    if data2 is None:
        dictObject["assignee"] = ""
    else:
        dictObject["assignee"] = position["fields"]["assignee"]["name"]


    dictObject["status"] = position ["fields"]["status"]["name"]
    dictObject["issueType"] = position ["fields"]["issuetype"]["name"]
    dictObject["resolution"] = position ["fields"]["resolutiondate"]
    dictObject["created"] = position ["fields"]["created"]
    dictObject["updated"] = position ["fields"]["updated"]
    dictObject["summary"] = position ["fields"]["summary"]
   
    totalIssues +=1

    if dictObject["status"] == "Open" :
        openIssues +=1

    if dictObject["status"] == "Closed" :
        closedIssues +=1

    if dictObject["status"] == "Resolved" :
        resolvedIssues +=1

    if dictObject["status"] == "In Progress" :
        inProgressIssues +=1

    if dictObject["status"] == "Done Locally" :
        doneLocallyIssues +=1

    if dictObject["status"] == "Reopened" :
        reopenedIssues +=1

	json_refactor.append(dictObject)



data3 = {}
#yyyymmdd
#data3["date"] = time.strftime("20150805")
myDate = time.strftime("%d/%m/%Y")
data3["date"] = myDate.replace("/", "")
data3["issues"] = json_refactor
json_data = json.dumps(data3)

#print json_data


#use the API to save JSON
url = "http://sincro.esinergy.com:9000/api/test"
response = urllib2.urlopen(url, json_data).read()
#print response



##pruebaaaa
#contando por tipo de issue
progresoDone = (closedIssues+resolvedIssues+doneLocallyIssues)/(1.0*totalIssues)*(100.00)
totalDone = (closedIssues+resolvedIssues+doneLocallyIssues)
totalPending = (openIssues+inProgressIssues+reopenedIssues)

#Metric JSON
metricJSONobject = {}
metricJSONobject["date"] = myDate.replace("/", "")
metricJSONobject["open"] = openIssues
metricJSONobject["closed"] = closedIssues
metricJSONobject["in_progress"] = inProgressIssues
metricJSONobject["resolved"] = resolvedIssues
metricJSONobject["done_locally"] = doneLocallyIssues
metricJSONobject["reopened"] = reopenedIssues
metricJSONobject["total_done"] = totalDone
metricJSONobject["total_pending"] = totalPending
metricJSONobject["total_issues"] = totalIssues
metricJSONobject["progress_done"] = progresoDone
metricJSONobject["progress_pending"] = (100.0-progresoDone)

jsonMetric = json.dumps(metricJSONobject)
#print jsonMetric

url2 = "http://sincro.esinergy.com:9000/api/metric"
response2 = urllib2.urlopen(url2, jsonMetric).read()
#print response2


myDatetime = time.strftime("%d/%m/%Y %H:%M")
f = open("/root/code/jirabot/logger.txt","a")
f.write("Jirabot saved " + myDatetime + '\n')
f.close()


