import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import subprocess
import os
import requests
import time 
import wikipedia
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import Tk, Label, Entry, Button, Text

# Initialize the speech engine
engine = pyttsx3.init('sapi5')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5  # Reduce pause threshold to make it more responsive
        r.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise
        try:
            audio = r.listen(source, timeout=5)  # Set timeout for listening
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"User said: {query}\n")
    except Exception as e:
        return "None"

    return query

def is_connected():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

def send_email(to, content):
    sender_email = "patelmanan074@gmail.com"  # Replace with your email
    password = "pqcf gwjd lcfv gmax"  # Replace with your app password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to
    msg['Subject'] = "Automated Email"
    msg.attach(MIMEText(content, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, to, text)
        server.quit()
        speak("Email has been sent successfully.")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send the email.")

def get_receiver_email():
    def submit_email():
        global receiver_email
        receiver_email = email_entry.get()
        root.destroy()

    root = Tk()
    root.title("Email Input")
    root.geometry("300x100")

    Label(root, text="Enter receiver's email:").pack(pady=5)
    email_entry = Entry(root, width=30)
    email_entry.pack(pady=5)
    Button(root, text="Submit", command=submit_email).pack(pady=5)

    root.mainloop()

def get_email_content():
    def submit_content():
        global email_content
        email_content = content_entry.get("1.0", "end-1c")
        root.destroy()

    root = Tk()
    root.title("Email Content Input")
    root.geometry("400x300")

    Label(root, text="Enter email content:").pack(pady=5)
    content_entry = Text(root, width=50, height=10)
    content_entry.pack(pady=5)
    Button(root, text="Submit", command=submit_content).pack(pady=5)

    root.mainloop()

if __name__ == '__main__':
    connection_status = is_connected()
    if connection_status:
        wishMe()

    spoke_disconnected = False  # Flag to track if disconnection message has been spoken
    spoke_connected = connection_status  # Flag to track if connection message has been spoken

    while True:
        current_status = is_connected()
        if current_status and not connection_status:
            if not spoke_connected:
                print("Connected to the internet.")
                speak("Connected to the internet.")
                wishMe()
                spoke_connected = True  # Set the flag to avoid repeating the message
                spoke_disconnected = False  # Reset the disconnection flag

        if current_status:
            query = takecommand().lower()

            if query == "none":
                continue

            # Wikipedia search functionality
            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                try:
                    results = wikipedia.summary(query, sentences=1)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                except wikipedia.DisambiguationError:
                    speak("Multiple options found. Please be more specific.")
                except wikipedia.PageError:
                    speak("No information found.")

            # Open YouTube
            elif 'open youtube' in query or 'open the youtube' in query:
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com")

            # Report current time
            elif 'what is the time' in query or 'what time is it' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {strTime}")

            # Open Visual Studio Code
            elif 'open vs code' in query or 'open visual studio code' in query:
                path = "C:\\Users\\patel\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(path)

            # Send an email
            elif 'send mail' in query or 'send email' in query:
                get_receiver_email()  # Get the receiver's email through a GUI
                get_email_content()  # Get the email content through a GUI
                send_email(receiver_email, email_content)

            # Stop the loop
            elif 'stop' in query:
                break

        else:
            if connection_status and not spoke_disconnected:
                print("Lost internet connection. Stopping recognition.")
                speak("Lost internet connection. Stopping recognition.")
                spoke_disconnected = True  # Set the flag to avoid repeating the message
                spoke_connected = False  # Reset the connection flag
            elif not connection_status and not spoke_disconnected:
                print("No internet connection. Please connect to the internet.")
                speak("No internet connection. Please connect to the internet.")
                spoke_disconnected = True  # Set the flag to avoid repeating the message
                spoke_connected = False  # Reset the connection flag

        connection_status = current_status
        time.sleep(2)  # Reduce sleep time for more frequent checks
