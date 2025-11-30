import json
import os
import requests
import time
from . import PayloadsGenerator
from . import BCNotesGenerator

# 打开proxies文件，导入代理
with open(os.getcwd().rsplit("/", 0)[0] + "/proxies.json") as json_profile:
    proxies = json.load(json_profile)

# 创建ticket
def createChange(startTime, endTime, isWinter, pet, assignee, validCircuitsList):

    BCNotes = BCNotesGenerator.getBCNotes(pet, validCircuitsList)

    payloads = PayloadsGenerator.getPayloads(startTime, endTime, isWinter, assignee, BCNotes, validCircuitsList)

    createChangeUrl = "https://ebaysnow.vip.ebay.com/api/message/send"

    createChangeHeaders = {
        "Content-Type" : "application/json",
        "Accept" : "application/json",
        "Authorization" : "Basic dV9zYV9lYmF5X3Nub3dfbmV0OlJlc3RpbnBlYWNldHJhY2UyMDIw"
    }

    response = requests.post(createChangeUrl, headers = createChangeHeaders, json = payloads, verify = "/usr/share/ca-certificates/eBayROOT/eBay_ROOT_CA.crt")

    uiLink = json.loads(response.text)["ui_link"]

    print("SNOW URL: " + uiLink)

#    targetLink = json.loads(response.text)["target_link"]


# 获取Change信息sys_id和change_number
# def getChangeInfo(targetLink, uiLink):

#     print("Getting Change Number")

#     time.sleep(10)

#     headers = {
#         "Content-Type" : "application/json",
#         "Accept" : "application/json",
#         "Authorization" : "Basic dV9zYV9lYmF5X3Nub3dfbmV0OlJlc3RpbnBlYWNldHJhY2UyMDIw"
#     }

#     response = requests.get(targetLink, headers = headers, proxies = proxies)

#     sysId = json.loads(response.text)["result"][0]["sys_id"]
#     changeNumber = json.loads(response.text)["result"][0]["number"]

#     print("Change Number Is: " + changeNumber)
#     print("SNOW URL: " + uiLink)

#     return sysId, changeNumber

# 上传附件
# def uploadAttachment(sysId, changeNumber, pet, validCircuitsList):

#     BCNotesGenerator.getBCNotes(pet, validCircuitsList, changeNumber)

#     print("Ready To Upload BC Notes")

#     time.sleep(10)

#     url = "https://ebayinc.service-now.com/api/now/attachment/file?table_name=change_request&table_sys_id=" + sysId + "&file_name=" + changeNumber + ".txt"

#     headers = {
#         "Content-Type" : "text/plain",
#         "Accept" : "application/json",
#         "verify" : "True",
#         "Authorization" : "Basic dV9zYV9lYmF5X3Nub3dfbmV0OlJlc3RpbnBlYWNldHJhY2UyMDIw"
#     }

#     print("Uploading BC Notes")

#     with open(os.getcwd().rsplit("/", 0)[0] + "/" + changeNumber + ".txt", 'r') as BCNotes:
#         files = {
#             "file" : BCNotes
#         }
#         requests.post(url, headers = headers, files = files, proxies = proxies)

#     print("Uploaded")

#     print("Detelting Local File")

#     if os.path.exists(os.getcwd().rsplit("/", 0)[0] + "/" + changeNumber + ".txt"):
#         os.remove(os.getcwd().rsplit("/", 0)[0] + "/" + changeNumber + ".txt")
#         print("Local File Is Deleted")
#     else:
#         print("Local File Does Not Exist")
