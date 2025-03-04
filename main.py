import os
from os import path
import pickle
from bs4 import BeautifulSoup 
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

NO_OF_NOTIFICATION_TO_BE_CHECKED = 3

# smtp connection
def Sendemail(date,Notification, link,receivers_email):
  # Define email addresses to use
    sender_email = os.environ.get('SMTP_SENDER_EMAIL')#sender email
    smtp_pass = os.environ.get('SMTP_PASSWORD')# app generated password
    # print(receivers_email)
    # receivers_email =os.environ.get('SMTP_RECEIVER_EMAIL')# receiver email


    # Define SMTP email server details
    smtp_server = 'smtp.gmail.com'

    # Construct email
    msg = MIMEMultipart('alternative')
    msg['To'] =receivers_email
    msg['From'] = sender_email
    msg['Subject'] = 'Latest GTU Notification'

    # Create the body of the message (a plain-text and an HTML version).
    html = (date + '\n'+Notification+ '\n'+link)



    part1 = MIMEText(html, 'html')

    msg.attach(part1)

    # Send the message via an SMTP server
    s = smtplib.SMTP(smtp_server,587)
    s.ehlo()
    s.starttls()
    s.login(sender_email,smtp_pass)
    print("successful connected")
    s.sendmail(sender_email, receivers_email, msg.as_string())
    s.quit()



r = requests.get("https://www.gtu.ac.in/Circular.aspx")

try:
    html = BeautifulSoup(r.text,'html.parser')
except Exception as e:
    print(e)

#memory of code 

l =os.environ.get('EMAIL_LIST')
class Record:

    target = 'Last_notification'

if path.exists("Record"):
    # load
    print("path exits")
    with open("Record", 'rb') as f:
            recorded = pickle.load(f)
            print("Last stored Link :"+recorded)


def Convert(string):
    li = list(string.split(","))
    return li

L = Convert(l)
def info():

    #date
    notificationToBeAddedFrom = NO_OF_NOTIFICATION_TO_BE_CHECKED
    for index in range(NO_OF_NOTIFICATION_TO_BE_CHECKED,0,-1):
        h3_tag = html.find("p",{"id":"ContentPlaceHolder1_lvCircular_lblUploadDate_" + str(index - 1)}).parent.find("h3",{"class":"d-block"})
        dt = (html.find("p",{"id":"ContentPlaceHolder1_lvCircular_lblUploadDate_" + str(index - 1)})).text
        link_tag=h3_tag.find("a",{"target" :"_blank"},href=True)
        link= link_tag.get('href')
        if(link==recorded): # if link matches to already recorded, from here on all notifications are new
            notificationToBeAddedFrom = index - 1
            break
    
    if(notificationToBeAddedFrom != 0):
        print("No of new notifications came -  " + str(notificationToBeAddedFrom))
        for index in range(notificationToBeAddedFrom,0,-1):
            h3_tag = html.find("p",{"id":"ContentPlaceHolder1_lvCircular_lblUploadDate_" + str(index - 1)}).parent.find("h3",{"class":"d-block"})
            dt = (html.find("p",{"id":"ContentPlaceHolder1_lvCircular_lblUploadDate_" + str(index - 1)})).text
            link_tag=h3_tag.find("a",{"target" :"_blank"},href=True)
            link= link_tag.get('href')
            print("Current Link :"+link)
            if recorded != link:
                try:
                    # msg = (dt + "\n\n"+link_tag.text+ "\n\n"+link + "\n")
                    for email in L:
                        Sendemail(dt,link_tag.text,link,email)
                        print("Mail sended successfully")
                    
                    with open("Record", 'wb') as f:
                        pickle.dump(link, f)
                        print("link is Successfully added to code memory")
                
                except Exception as e:
                    print("Error : ")
                    print(e)
    else:
        print("No latest notification")



if __name__ == "__main__":
    info()

           