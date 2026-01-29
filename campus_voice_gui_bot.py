import tkinter as tk
import speech_recognition as sr
import pyttsx3
from datetime import datetime

# ---------------- DATA ----------------
timetable = {
    "monday": ["9AM - Math", "11AM - DSA", "2PM - Physics"],
    "tuesday": ["10AM - DBMS", "1PM - DSA Lab"],
    "wednesday": ["9AM - Math", "12PM - OS"],
    "thursday": ["10AM - DSA", "2PM - DBMS"],
    "friday": ["9AM - Physics", "11AM - Math"]
}

exams = {
    "dsa": "25 Feb 2026",
    "dbms": "28 Feb 2026",
    "math": "2 Mar 2026"
}

canteen_menu = {
    "monday": ["Idli", "Sambar", "Rice", "Curd"],
    "tuesday": ["Dosa", "Chutney", "Veg Biryani"],
    "wednesday": ["Pasta", "Garlic Bread"],
    "thursday": ["Fried Rice", "Manchurian"],
    "friday": ["Noodles", "Spring Rolls"]
}

events = [
    "Tech Fest - 30 Jan",
    "Cultural Day - 5 Feb",
    "Sports Meet - 12 Feb"
]

reminders = []

# ---------------- SPEECH SETUP ----------------
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_voice():
    with sr.Microphone() as source:
        chat_box.insert(tk.END, "\n🎤 Listening...\n")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            chat_box.insert(tk.END, f"🗣️ You (voice): {command}\n")
            return command
        except:
            chat_box.insert(tk.END, "❌ Sorry, I didn't catch that.\n")
            speak("Sorry, I didn't catch that.")
            return ""

# ---------------- BOT LOGIC ----------------
def bot_reply(user_input):
    user_input = user_input.lower()

    if "timetable" in user_input or "class" in user_input:
        if "today" in user_input:
            day = datetime.now().strftime("%A").lower()
        else:
            day = user_input.split()[-1]
        if day in timetable:
            reply = f"📅 Timetable for {day.capitalize()}:\n"
            for c in timetable[day]:
                reply += "- " + c + "\n"
        else:
            reply = "❌ No timetable found for that day."

    elif "exam" in user_input:
        words = user_input.split()
        subject = words[-2] if len(words) >= 2 else ""
        if subject in exams:
            reply = f"📝 {subject.upper()} exam is on {exams[subject]}"
        else:
            reply = "❌ No exam found for that subject."

    elif "menu" in user_input or "canteen" in user_input:
        day = datetime.now().strftime("%A").lower()
        if day in canteen_menu:
            reply = "🍽️ Today's Canteen Menu:\n"
            for item in canteen_menu[day]:
                reply += "- " + item + "\n"
        else:
            reply = "❌ No menu found for today."

    elif "event" in user_input:
        reply = "🎉 Upcoming Events:\n"
        for e in events:
            reply += "- " + e + "\n"

    elif "remind me to" in user_input:
        try:
            parts = user_input.replace("remind me to", "").split("at")
            task = parts[0].strip()
            time_str = parts[1].strip()
            remind_time = datetime.strptime(time_str, "%H:%M")
            remind_time = remind_time.replace(
                year=datetime.now().year,
                month=datetime.now().month,
                day=datetime.now().day
            )
            reminders.append((task, remind_time))
            reply = f"⏰ Reminder set for '{task}' at {time_str}"
        except:
            reply = "❌ Use format: remind me to <task> at HH:MM"

    elif "exit" in user_input or "quit" in user_input:
        reply = "👋 Bye! You can close the window."

    else:
        reply = "🤖 Sorry, I didn’t understand that."

    return reply

def check_reminders():
    now = datetime.now()
    for r in reminders[:]:
        task, r_time = r
        if now >= r_time:
            chat_box.insert(tk.END, f"\n🔔 REMINDER: {task}\n")
            speak(f"Reminder: {task}")
            reminders.remove(r)

    root.after(1000, check_reminders)

# ---------------- GUI FUNCTIONS ----------------
def send_message():
    user_input = user_entry.get()
    if not user_input.strip():
        return

    chat_box.insert(tk.END, f"\n🧑 You: {user_input}\n")
    reply = bot_reply(user_input)
    chat_box.insert(tk.END, f"🤖 Bot: {reply}\n")
    speak(reply)

    user_entry.delete(0, tk.END)

def voice_input():
    command = listen_voice()
    if command:
        reply = bot_reply(command)
        chat_box.insert(tk.END, f"🤖 Bot: {reply}\n")
        speak(reply)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("CampusBuddy - Voice + GUI Bot")
root.geometry("550x650")

chat_box = tk.Text(root, bg="#f2f2f2", font=("Arial", 11))
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

user_entry = tk.Entry(root, font=("Arial", 12))
user_entry.pack(padx=10, pady=5, fill=tk.X)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

send_btn = tk.Button(btn_frame, text="Send", width=12, command=send_message)
send_btn.pack(side=tk.LEFT, padx=5)

voice_btn = tk.Button(btn_frame, text="🎤 Speak", width=12, command=voice_input)
voice_btn.pack(side=tk.LEFT, padx=5)

chat_box.insert(tk.END, "🎓 Welcome to CampusBuddy!\n")
chat_box.insert(tk.END, "You can type or click 🎤 Speak.\n")
chat_box.insert(tk.END, "Try:\n")
chat_box.insert(tk.END, "- What’s my timetable today\n")
chat_box.insert(tk.END, "- When is the DSA exam\n")
chat_box.insert(tk.END, "- Show today’s canteen menu\n")
chat_box.insert(tk.END, "- Show events\n")
chat_box.insert(tk.END, "- Remind me to submit assignment at 18:30\n\n")

check_reminders()
root.mainloop()
