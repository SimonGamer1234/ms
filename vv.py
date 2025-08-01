import os
import random
import requests
import time
import json

# Retrieve the environment variables
TOKEN1 = os.getenv("ACCOUNT1")
TOKEN2 = os.getenv("ACCOUNT2")
TOKEN3 = os.getenv("ACCOUNT3")
TOKEN4 = os.getenv("ACCOUNT4")
BOT_TOKEN = os.getenv("BOT_TOKEN")
NOTIONKEY = os.getenv("NOTIONKEY")
G_TOKEN = os.getenv("G_TOKEN")
DatabaseID = os.getenv("DatabaseID")
ADS = os.getenv("ADS")
URLS = os.getenv("URLS").split(",")
AD_TYPE = os.getenv("AD_TYPE")
FileName = "tracker.txt"
REPOSITORY = os.getenv("GITHUB_REPOSITORY")
REPO_OWNER, REPO_NAME = REPOSITORY.split("/")
print(f"REPO_OWNER: {REPO_OWNER}, REPO_NAME: {REPO_NAME}")
BASE_VARIABLE = os.getenv("BASE_VARIABLE")
BASE_VARIABLE = f"{BASE_VARIABLE}\n=divider=\nBase_Variable\n=divider=\nBase_Variable\n=divider=\nBase_Variable\n=divider=\nBase_Variable\n=divider=\nBase_Variable"
Errors = []

def GetVariableName(AD_TYPE):
    if AD_TYPE == "Normal":
        return "NORMAL_ADS"
    elif AD_TYPE == "Aviation":
        return "AVIATION_ADS"
    else:
        print("Invalid AD_TYPE. Please choose 'Normal' or 'Aviation'.")
        exit(1)

def ge_current_ad_number(AD_TYPE):
    def GetInfoFromFile(filename):
        with open(filename, "r") as file:
            content = str(file.read())
            AdSplit1 = content.split("\n=divider=\n")
            AdSplit2 = content.split("\r\n=divider=\r\n")
            if len(AdSplit1) > 1:
                NormalAd = AdSplit1[0]
                AviationAd = AdSplit1[1]
            elif len(AdSplit2) > 1:
                NormalAd = AdSplit2[0]
                AviationAd = AdSplit2[1]
            else:
                NormalAd = "0"
                AviationAd = "0"
        return NormalAd, AviationAd
    def EditFile(filename):
        if AD_TYPE == "Normal":
            NormalAd, AviationAd = GetInfoFromFile(filename)
            if int(NormalAd) == 11:
                NormalAd = 0
            else:
                NormalAd = int(NormalAd) + 1
            with open(filename, "w") as file:
                file.write(f"{NormalAd}\n=divider=\n{AviationAd}")
            NormalAd, AviationAd = GetInfoFromFile(filename)
        elif AD_TYPE == "Aviation":
            NormalAd, AviationAd = GetInfoFromFile(filename)
            if int(AviationAd) == 8:
                AviationAd = 0
            else:
                AviationAd = int(AviationAd) + 1
            with open(filename, "w") as file:
                file.write(f"{NormalAd}\n=divider=\n{AviationAd}")
            NormalAd, AviationAd = GetInfoFromFile(filename)
        else:
            print("Invalid AD_TYPE. Please choose 'Normal' or 'Aviation'.")
            exit(1)
    def GetAd(AD_TYPE):
        if AD_TYPE == "Normal":
            NormalAd, AviationAd = GetInfoFromFile(FileName)
            return int(NormalAd)
        elif AD_TYPE == "Aviation":
            NormalAd, AviationAd = GetInfoFromFile(FileName)
            return int(AviationAd)
        else:
            print("Invalid AD_TYPE. Please choose 'Normal' or 'Aviation'.")
            exit(1)
    AdNumber = GetAd(AD_TYPE)
    EditFile(FileName)
    return AdNumber

def GetCurrentAd(AdNumber):
  SplittedAds1 = ADS.split("\n\n++SPLITTER++\n\n")
  SplittedAds2 = ADS.split("\r\n\r\n++SPLITTER++\r\n\r\n")
  if len(SplittedAds1) > 1:
    print("SplittedAds1:", SplittedAds1)
    return SplittedAds1, SplittedAds1[AdNumber]  
  elif len(SplittedAds2) > 1:
    print("SplittedAds2:", SplittedAds2)
    return SplittedAds2, SplittedAds2[AdNumber]
  else:
    print("Error: No ads found in the provided string.")
  
def GetToken(AdNumber):
    if AD_TYPE == "Normal":
        TOKENS = [TOKEN1, TOKEN2, TOKEN3, TOKEN4]
    elif AD_TYPE == "Aviation":
        TOKENS = [TOKEN1, TOKEN2, TOKEN3]
    else:
        print("Invalid AD_TYPE. Please choose 'Normal' or 'Aviation'.")
    Token = TOKENS[AdNumber % len(TOKENS)]
    return Token  

def SetContent(Ad):
    SplittedAd1 = Ad.split("\n=divider=\n")
    print(SplittedAd1)
    SplittedAd2 = Ad.split("\r\n=divider=\r\n")
    print(SplittedAd2)
    if len(SplittedAd1) > 1:
        content = SplittedAd1[0]
        variation = SplittedAd1[1]
        total_posts = SplittedAd1[2]
        postings = SplittedAd1[3]
        keywords = SplittedAd1[4]
        channel_ID = SplittedAd1[5]
    elif len(SplittedAd2) > 1:
        content = SplittedAd2[0]
        variation = SplittedAd2[1]
        total_posts = SplittedAd2[2]
        postings = SplittedAd2[3]
        keywords = SplittedAd2[4]
        channel_ID = SplittedAd2[5]
    else:
        print("Error: No ad content found in the provided string.")
    print(f"Content: {content}, Variation: {variation}, Total Posts: {total_posts}, Postings Left: {postings}, Keywords: {keywords}, Channel ID: {channel_ID}")
    return content, variation, total_posts, postings, keywords, channel_ID
def EditPostingsLeft(PostingsLeft, Keywords, AdNumber, SplittedAds, VariableName): # Edits the postings left for the ad, and updates the variable in Github Actions.

    def UpdateAdVariable(VariableName, Ad): # Updates the whole variable in Github Actions
        print(f"Updating variable {Ad}")
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/variables/{VariableName}"
        print(url)
        headers = {
        "Authorization": f"Bearer {G_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
        }

        payload = {
            "value": Ad
        }

        response = requests.patch(url, headers=headers, json=payload)

        # Results
        print(response.text)
        if response.status_code == 204:
            print("✅ Variable updated successfully.")
        elif response.status_code == 404:
            print("❌ Variable not found. You may need to create it first.")
            print(response.text)
        else:
            print(f"❌ Failed to update variable. Status code: {response.status_code}")
            print(response.text)

    def EditAllPostings(SplittedAds, LocalPostingsLeft, Keywords): # Edits postings for all the ads, by searching for same keywords.
        print(f"Editing all postings with {LocalPostingsLeft} left for keywords: {Keywords}")
        print(f"Total ads to edit: {len(SplittedAds)}")
        print(SplittedAds)
        for ad in SplittedAds:
            ad_parts1 = ad.split("\n=divider=\n")
            ad_parts2 = ad.split("\r\n=divider=\r\n")
            if len(ad_parts1) > 1:
                ad_parts = ad_parts1
            elif len(ad_parts2) > 1:
                ad_parts = ad_parts2
            else:
                print("Error: No ad content found in the provided string.")
                exit(1)
            Keywords2 = ad_parts[4]
            if Keywords == Keywords2:
                print(f"Editing ad: {ad_parts[0]}")
                ad_parts[3] = str(LocalPostingsLeft)
                ad1 = "\n=divider=\n".join(ad_parts)
                SplittedAds[SplittedAds.index(ad)] = ad1
            else:
                print(f"Skipping ad: {ad_parts[0]} as it does not match the keywords.")
                continue
        NewVariable = "\n\n++SPLITTER++\n\n".join(SplittedAds)
        return NewVariable
    
    def RemoveAds(SplittedAds, Keywords): # Removes ads with the same keywords, if the postings left is 0.
        removing = []
        for ad in SplittedAds:
            ad_parts1 = ad.split("\n=divider=\n")
            ad_parts2 = ad.split("\r\n=divider=\r\n")
            if len(ad_parts1) > 1:
                ad_parts = ad_parts1
            elif len(ad_parts2) > 1:
                ad_parts = ad_parts2
            else:
                print("Error: No ad content found in the provided string.")
                exit(1)
            if ad_parts[4] == Keywords:
                ad_position = SplittedAds.index(ad)
                removing.append(ad_position)
                ad1 = BASE_VARIABLE
                SplittedAds[SplittedAds.index(ad)] = ad1
        Variable = "\n\n++SPLITTER++\n\n".join(SplittedAds)
        return Variable, removing
    
    def main(): # Main function to edit the postings left for the ad, based on the postings left.
        NewPostingsLeft = int(PostingsLeft) - 1
        print(f"New postings left: {NewPostingsLeft}")
        if  NewPostingsLeft > 0:
            Removed = 0
            Variable = EditAllPostings(SplittedAds, NewPostingsLeft, Keywords)
            UpdateAdVariable(VariableName, Variable)
            return Removed, None
        elif NewPostingsLeft == 0:
            Variable, removing = RemoveAds(SplittedAds, Keywords)
            Removed = 1      
            UpdateAdVariable(VariableName,Variable)
            return Removed,removing
    
    Removed, removing = main()
    return Removed, removing



        
def SendMessageFromAccount(Token, ChannelID, Content):
    token_index = [TOKEN1, TOKEN2, TOKEN3, TOKEN4].index(Token)
    header = {"Authorization": Token}
    payload = {"content": Content}
    link = f"https://discord.com/api/v9/channels/{ChannelID}/messages"
    try:
        res = requests.post(link, data=payload, headers=header)
        print(f"Posted to {link} : {res.status_code}")  # Print response status
        print(res.text)
        if res.status_code != 200:
            Errors.append((link, res.status_code, token_index, AD_TYPE))
        return res.status_code, Errors
    except requests.RequestException as e:
        print(f"Error posting to {link}: {e}")
        return None

def SendMessageFromBot(BotToken, ChannelID, Content):
    header = {"Authorization": f"Bot {BotToken}"}
    payload = {"content": Content}  
    link = f"https://discord.com/api/v9/channels/{ChannelID}/messages"
    try:
        res = requests.post(link, json=payload, headers=header)
        print(f"Posted to {link} : {res.status_code}")  # Print response status
        if res.status_code != 200:
            print(f"Error posting to {link}: {res.status_code} with Bot")
        return res.status_code, res.text
    except requests.RequestException as e:
        print(f"Error posting to {link}: {e}")
        return None
    

def Posting(Ids, Content, Token):
    unauthorized = 0
    for ID in Ids:
        sleeptime = random.uniform(2, 3)
        time.sleep(sleeptime)  # Sleep for a random time between 2 and 3 seconds
        status_code, Errors = SendMessageFromAccount(Token, ID, Content)
        if status_code == 401:
            unauthorized = 1
            break  # Stop if unauthorized
    return unauthorized, Errors

def ReportMainChannel(unauthorized, Content, Errors, Token):
    token_index = [TOKEN1, TOKEN2, TOKEN3, TOKEN4].index(Token)
    if unauthorized == 1:
        ReportContent = f"TOKEN {token_index} UNAUTHORIZED - {AD_TYPE} - <@1148657062599983237>\n\nContent: {Content}"
    else:
        ReportContent = f" {str(Errors)}\n\nContent: {Content}"
    MessageStatus, MessageText = SendMessageFromBot(BOT_TOKEN, "1300080115945836696", ReportContent)
    return MessageStatus, MessageText
    
def SetVauesByVariation(Variation):
    if Variation == "Free":
        Postings = 9
    elif Variation == "Basic":
        Postings = 14
    elif Variation == "Advanced":
        Postings = 21
    elif Variation == "Pro":
        Postings = 28
    elif Variation == "God's": 
        Postings = 42
    else:
        print("Something went wrong with Variation")    
    return Postings

def ReportTicket(Removed, TicketID, unauthorized, PostingsTotal, PostingsLeft):
    if unauthorized == 1:
        ReportContent = f"There was a porblem with the ad posting. The Owner has been notified. He will provide more info <@1148657062599983237>"
    else:
        if Removed == 1:
            ReportContent = "We have finished posting your ad. <@1148657062599983237>"
        else:
            ReportContent = f"We have posted your ad. The posting was successful.  {PostingsLeft} / {PostingsTotal}"
    MessageStatus = SendMessageFromBot(BOT_TOKEN, TicketID, ReportContent)
    return MessageStatus
    
def EditNotionMenu(Keywords, WhichVar, DatabaseID):
    WhichVar = WhichVar.split(",")
    for Var in WhichVar:
        Var = int(Var.strip())
        headers = {
            'Authorization': f"Bearer {NOTIONKEY}",
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json',
        }

        json = {
            "sorts": [
            {
                "property": "Name",
                "direction": "ascending"
            }, 
            ],
        }
        response1 = requests.post(
            f'https://api.notion.com/v1/databases/{DatabaseID}/query',
            headers=headers, json=json
        )

        data = response1.json()
        results = data.get('results', [])
        object = results[Var-1]
        properties = object.get('properties', {})
        newname = f"{Var} | {Keywords}"
        properties['Name']['title'][0]['text']['content'] = newname

        # Update the object with the new name
        update_url = f"https://api.notion.com/v1/pages/{object['id']}"
        json = {
            'properties': {
                'Name': {
                    'title': [
                        {
                            'text': {
                                'content': newname
                            }
                        }
                    ]
                }
            }
        }
        response2 = requests.patch(update_url, headers=headers, json=json)
        if not response2.status_code or not response1.status_code == 200:
            print("PROBLEM WITH NOTION")
            print(response2.status_code, response1.status_code)

def main():
    VariableName = GetVariableName(AD_TYPE)
    AdNumber = ge_current_ad_number(AD_TYPE)
    SplittedAds, CurrentAd = GetCurrentAd(AdNumber)
    Token = GetToken(AdNumber)
    Content, Variation, TotalPosts, PostingsLeft, Keywords, ChannelID = SetContent(CurrentAd)
    unauthorized, Errors = Posting(URLS, Content, Token)
    if Variation == "Base_Variable":
        MessageStatus, MessageText = ReportMainChannel(unauthorized, Content, Errors, Token)
        ReportTicketStatus = ReportTicket(0, 1387532585462272120, unauthorized, "Base", "Base")
    else:
        Removed, removing = EditPostingsLeft(PostingsLeft, Keywords, AdNumber, SplittedAds, VariableName)
        Postings = SetVauesByVariation(Variation)
        MessageStatus, MessageText = ReportMainChannel(unauthorized, Content, Errors, Token)
        ReportTicketStatus = ReportTicket(Removed, ChannelID, unauthorized, Postings, PostingsLeft)
        if Removed == 1:
            EditNotionMenu("Base Variable (free space)", removing, DatabaseID)
    if MessageStatus == 200 and ReportTicketStatus == 200:
        print("All messages posted successfully.")
    else:
        print("There was an error posting some messages.")
        if MessageStatus != 200:
            print(f"Main channel report failed with status code: {MessageStatus, MessageText}")
        if ReportTicketStatus != 200:
            print(f"Ticket report failed with status code: {ReportTicketStatus}")



    
main()