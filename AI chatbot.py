import pyautogui
import time
import pyperclip
import openai


openai.api_key = "YOUR_OPENAI_API_KEY"   # 🔑 Put your API key here

TARGET_USER = "Rohan Das"
BOT_NAME = "Naruto"

CHECK_INTERVAL = 8  
CHROME_ICON = (200, 1050)
CHAT_AREA_START = (300, 200)
CHAT_AREA_END = (1200, 800)
CHAT_INPUT_BOX = (600, 900)



def open_chat_application():
    pyautogui.click(CHROME_ICON)
    time.sleep(5)


def copy_chat_history():
    pyautogui.moveTo(CHAT_AREA_START)
    pyautogui.dragTo(CHAT_AREA_END, duration=1, button='left')
    pyautogui.hotkey("ctrl", "c")
    time.sleep(1)
    return pyperclip.paste()


def is_last_message_from_target(chat_text):
    lines = chat_text.strip().split("\n")
    if not lines:
        return False
    return TARGET_USER in lines[-1]


def generate_funny_reply(chat_history):
    prompt = f"""
You are {BOT_NAME}, a savage but funny anime character.
Roast people humorously without being offensive.

Chat History:
{chat_history}

Reply in a short, witty roast.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a funny roast chatbot."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=80
    )

    return response["choices"][0]["message"]["content"]


def send_message(message):
    pyperclip.copy(message)
    pyautogui.click(CHAT_INPUT_BOX)
    time.sleep(1)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")


def main():
    open_chat_application()
    print("🤖 Naruto AI Chatbot Activated!")

    while True:
        try:
            chat_history = copy_chat_history()

            if is_last_message_from_target(chat_history):
                print("🎯 Message detected from target user!")
                reply = generate_funny_reply(chat_history)
                send_message(reply)
                print("🔥 Roast sent successfully!")

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print("⚠️ Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    main()
