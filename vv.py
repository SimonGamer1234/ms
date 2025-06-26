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
G_TOKEN = os.getenv("G_TOKEN")
ADS = os.getenv("ADS")
URLS = os.getenv("URLS").split(",")
AD_TYPE = os.getenv("AD_TYPE")
FileName = "tracker.txt"


def ge_current_ad_number(AD_TYPE):
    def GetInfoFromFile(filename):
        with open(filename, "r") as file:
            content = str(file.read())
            print(f"Content of {filename}: {content}")
            AdSplit1 = content.split("\n=divider=\n")
            AdSplit2 = content.split("\r\n=divider=\r\n")
            if len(AdSplit1) > 1:
                print("First")
                NormalAd = AdSplit1[0]
                AviationAd = AdSplit1[1]
            elif len(AdSplit2) > 1:
                print("Second")
                NormalAd = AdSplit2[0]
                AviationAd = AdSplit2[1]
            else:
                print("Error: No ads found in the file.")
                NormalAd = "0"
                AviationAd = "0"
            print(f"Normal Ad: {NormalAd}")
            print(f"Aviation Ad: {AviationAd}")
        return NormalAd, AviationAd
    def EditFile(filename):
        if AD_TYPE == "Normal":
            NormalAd, AviationAd = GetInfoFromFile(filename)
            if NormalAd == 12:
                NormalAd = 0
            else:
                NormalAd = int(NormalAd) + 1
            print("Normal Ad: ", NormalAd)
            with open(filename, "w") as file:
                file.write(f"{NormalAd}\n=divider=\n{AviationAd}")
                print("File updated successfully.")
            NormalAd, AviationAd = GetInfoFromFile(filename)
            print(f"Updated Normal Ad: {NormalAd}")
            print(f"Updated Aviation Ad: {AviationAd}")
        elif AD_TYPE == "Aviation":
            NormalAd, AviationAd = GetInfoFromFile(filename)
            if AviationAd == 9:
                AviationAd = 0
            else:
                AviationAd = int(AviationAd) + 1
            print("Aviation Ad: ", AviationAd)
            with open(filename, "w") as file:
                file.write(f"{NormalAd}\n=divider=\n{AviationAd}")
                print("File updated successfully.")
            NormalAd, AviationAd = GetInfoFromFile(filename)
            print(f"Updated Normal Ad: {NormalAd}")
            print(f"Updated Aviation Ad: {AviationAd}")
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
  SplittedAds2 = ADS.split("\r\n\r\n++SPLITTER++\r\n")
  if len(SplittedAds1) > 1:
      return SplittedAds1[AdNumber]
  elif len(SplittedAds2) > 1:
      return SplittedAds2[AdNumber]
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
    SplittedAd2 = Ad.split("\r\n=divider=\r\n")
    if len(SplittedAd1) > 1:
        Content = SplittedAd1[0]
        TotalPosts = SplittedAd1[1]
        DaysLeft = SplittedAd1[2]
        Keywords = SplittedAd1[3]
        ChannelID = SplittedAd1[4]
    elif len(SplittedAd2) > 1:
        Content = SplittedAd2[0]
        TotalPosts = SplittedAd2[1]
        DaysLeft = SplittedAd2[2]
        Keywords = SplittedAd2[3]
        ChannelID = SplittedAd2[4]
    else:
        print("Error: No ad content found in the provided string.")
    return Content, TotalPosts, DaysLeft, Keywords, ChannelID

    

def SendMessageFromAccount(Token, ChannelID, Content):
    Errors = []
    token_index = [TOKEN1, TOKEN2, TOKEN3, TOKEN4].index(Token)
    header = {"Authorization": Token}
    payload = {"content": Content}
    link = f"https://discord.com/api/v9/channels/{ChannelID}/messages"
    try:
        res = requests.post(link, data=payload, headers=header)
        print(f"Posted to {link} : {res.status_code}")  # Print response status
        print(res.text)
        if res.status_code != 200:
            Errors.append((link, res.status_code, token_index, "Normal"))
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
        return res.status_code
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
        ReportContent = f"TOKEN {token_index} UNAUTHORIZED - Normal - <@1148657062599983237>\n\nContent: {Content}"
    else:
        ReportContent = f" {str(Errors)}\n\nContent: {Content}"
    MessageStatus = SendMessageFromBot(BOT_TOKEN, "1300080115945836696", ReportContent)
    return MessageStatus
    

def ReportTicket(TicketID, unauthorized):
    if unauthorized == 1:
        ReportContent = f"There was a porblem with the ad posting. The Owner has been notified. He will provide more info <@1148657062599983237>"
    else:
        ReportContent = f"We have posted your ad. The posting was successful."
    MessageStatus = SendMessageFromBot(BOT_TOKEN, TicketID, ReportContent)
    return MessageStatus
    

def main():
    AdNumber = ge_current_ad_number(AD_TYPE)
    CurrentAd = GetCurrentAd(AdNumber)
    Token = GetToken(AdNumber)
    Content, TotalPosts, DaysLeft, Keywords, ChannelID = SetContent(CurrentAd)
    unauthorized, Errors = Posting(URLS, Content, Token)
    MessageStatus = ReportMainChannel(unauthorized, Content, Errors, Token)
    ReportTicketStatus = ReportTicket(ChannelID, unauthorized)
    if MessageStatus == 200 and ReportTicketStatus == 200:
        print("All messages posted successfully.")
    else:
        print("There was an error posting some messages.")
        if MessageStatus != 200:
            print(f"Main channel report failed with status code: {MessageStatus}")
        if ReportTicketStatus != 200:
            print(f"Ticket report failed with status code: {ReportTicketStatus}")



    
main()