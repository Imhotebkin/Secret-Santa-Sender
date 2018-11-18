import re
import random
import codecs
import smtplib
from email.mime.text import MIMEText
from email.header import Header

email = "example@gmail.com"
password = "example"
smtpAdress = 'smtp.gmail.com'
smtpPort = 587

def randomize(people):
    shuffled = {}
    keys = list(people.keys())
    for key, value in people.items():
        while True:
            rkey =random.choice(keys)
            if rkey != key:
                if people[rkey] != 1:
                    shuffled[key]=people[rkey]
                    people[rkey]=1
                    break
    for key,value in shuffled.items():
        print(key,value)
    send(shuffled)
    return

def send(sendDict):
    server = smtplib.SMTP(smtpAdress, smtpPort)
    server.starttls()
    server.login(email, password)

    for key,value in sendDict.items():
        message = MIMEText(value,_charset="UTF-8")
        message['Subject']=Header("Secret Santa","utf-8")
        server.sendmail(email, key, message.as_string())
    server.quit()
    return

def readFile(filename):
    try:
        people = {}
        with codecs.open(filename,encoding='utf-8') as f:
            content = f.read().splitlines() 
            for line in content:                
                splits = str.split(line,',')
                if len(splits)>1:
                    if re.match("[^@]+@[^@]+\.[^@]+",splits[0]):
                        people[splits[0]]=splits[1]
                    else:
                        if re.match("[^@]+@[^@]+\.[^@]+",splits[1]):
                            people[splits[1]]=splits[0]
                        else:
                            print("No email found in line: "+line)
                else:
                    print("Invalid line format in line: "+line)
    except FileNotFoundError:
        print("input file not found")
        return
    randomize(people)
    return

random.seed(1234)
readFile("in.csv") 