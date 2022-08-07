import pyautogui as pt
from time import sleep
import pyperclip
import sklearn
import random
#import webbrowser
#from flask import Flask , render_template , request
import pickle
from playsound import playsound
from difflib import SequenceMatcher
import numpy as np
import subprocess
subprocess.Popen(["cmd", "/C", "start whatsapp://send?phone=+918075994774"], shell=True)


class pranav:
    def play():
        playsound("sound/IphoneWhatsappTone.mp3")
        return "Hi there,this is Mr.Bot I generate auto replies for general messages." 

# webbrowser.open('https://web.whatsapp.com')
model = pickle.load(open('model.pkl', 'rb'))
cv = pickle.load(open('vector.pkl', 'rb'))

greetings = {"Hi": "Hi", "Hello": "Hai", "Hi": "Hello", "Greetings!": "Hello", "Hello": "Greetings!", "Hi, How is it going?": "Good", "Hi, How is it going?": "Fine", "Hi, How is it going?": "Okay", "Hi, How is it going?": "Great", "Hi, How is it going?": "Could be better.", "Hi, How is it going?": "Not so great.", "How are you doing?": "Good.", "How are you doing?": "Very well, thanks.", "How are you doing?": "Fine, and you?", "Nice to meet you.": "Thank you.", "How do you do?": "I'm doing well.",
            "How do you do?": "I'm doing well. How are you?", "Hi, nice to meet you.": "Thank you. You too.", "It is a pleasure to meet you.": "Thank you. You too.", "Top of the morning to you!": "Thank you kindly.", "Top of the morning to you!": "And the rest of the day to you.", "What's up?": "Not much.", "What's up?": "Not too much.", "What's up?": "Not much, how about you?", "What's up?": "Nothing much.", "What's up?": "The sky's up but I'm fine thanks. What about you?","Thank you.":"Welcome"}

LIST = ["Hello", "Hi", "Hi", "Hello", "Greetings!", "Hello", "Hello", "Greetings!", "Hi, How is it going?", "Good", "Hi, How is it going?", "Fine", "Hi, How is it going?", "Okay", "Hi, How is it going?", "Great", "Hi, How is it going?", "Could be better.", "Hi, How is it going?", "Not so great.", "How are you doing?", "Good.", "How are you doing?", "Very well, thanks.", "How are you doing?", "Fine, and you?", "Nice to meet you.", "Thank you.", "How do you do?", "I'm doing well.",
        "How do you do?", "I'm doing well. How are you?", "Hi, nice to meet you.", "Thank you. You too.", "It is a pleasure to meet you.", "Thank you. You too.", "Top of the morning to you!", "Thank you kindly.", "Top of the morning to you!", "And the rest of the day to you.", "What's up?", "Not much.", "What's up?", "Not too much.", "What's up?", "Not much, how about you?", "What's up?", "Nothing much.", "What's up?", "The sky's up but I'm fine thanks. What about you?","Welcome"]

sleep(15)

position1 = pt.locateOnScreen("smiley_paperclip.png", confidence=0.6)
x = position1[0]
y = position1[1]

# position2 = pt.locateOnScreen("web_browser_logo.png", confidence=0.6)
# x = position2[0]
# y = position2[1]

# Gets message


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def check(str1):
    bool = False
    for i in LIST:
        i = i.lower()
        str1 = str1.lower()
        if similar(str1, i) > 0.8:
            bool = True
            break
    return bool


res = [*set(LIST)]


def checkpk(str1):
    for i in res:
        j = i.lower()
        str1 = str1.lower()
        if similar(str1, j) > 0.75:
            return i


def reply(str1):

    return greetings[checkpk(str1)]


# def play():
#     playsound("IphoneWhatsappTone.mp3")




def getmessage():
    global x, y

    position = pt.locateOnScreen("Smiley_paperclip.png", confidence=0.6)
    x = position[0]
    y = position[1]
    pt.moveTo(x, y, duration=0.5)
    pt.moveTo(x + 90, y - 60, duration=0.5)
    # if pt.pixelMatchesColor(int(x + 90),int(y - 70),(46, 198, 80),tolerance=10):
    pt.tripleClick()
    pt.rightClick()
    pt.moveRel(12, 15)
    pt.click()
    whatsapp_message = pyperclip.paste()
    pt.click()
    print("meassage received: " + whatsapp_message)

    return whatsapp_message


# Post
def post_response(message):
    global x, y

    position = pt.locateOnScreen("Smiley_paperclip.png", confidence=0.6)
    x = position[0]
    y = position[1]
    pt.moveTo(x + 200, y + 20, duration=0.5)
    pt.click()
    pt.typewrite(message, interval=0.01)

    pt.typewrite("\n", interval=0.01)

# Processes Response


def process_response(message):
    #random_no = random.randrange(3)
    data = [message]
    data = cv.transform(data).toarray()
    pred = model.predict(data)

    if pred == [1]:
        return "Pranav don't spam"
    else:
        if check(message) == True:
            return reply(message)
        else:
            return pranav.play()
            # if random_no == 0:
            #     return "That's cool"
            # elif random_no == 1:
            #     return "yeah"
            # else:
            #     return "Hmmm"


# Check for new message
def check_for_new_message():
    # global x, y
    # position = pt.locateOnScreen("web_browser_logo.png", confidence=0.6)
    # x = position[0]
    # y = position[1]
    pt.moveTo(x + 90, y - 60, duration=0.5)


while True:
    # Continuously check for the green point and new messages
    try:
        position = pt.locateOnScreen("green_point.png", confidence=0.7)

        if position is not None:
            pt.moveTo(position)
            pt.moveRel(-100, 0)
            pt.click()
            sleep(0.5)
            # post_response()

    except(Exception):
        print("No new messages found")

    if pt.pixelMatchesColor(int(x + 90), int(y - 60), (32, 44, 51), tolerance=10):
        print("is grey")
        processed_message = process_response(getmessage())
        post_response(processed_message)
    else:
        print("No new messages")
    # sleep(5)

    check_for_new_message()
