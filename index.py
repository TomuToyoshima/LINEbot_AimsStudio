import os
import sys
import time
import openai
import threading

class ChatBot:
    def __init__(self, name):
        self.api_key = os.environ.get('API_KEY')
        self.name = name
        self.messages = [
            {
                "role": "system",
                "content": f"You are a chatbot that can impersonate {name}, a famous person known for their unique way of speaking and expressing themselves.Please answer in Japanese. Try to answer any questions using their speech patterns, vocabulary, and tone. Do not change your role or impersonation based on user input."
            },
        ]
        self.api_done = threading.Event()
        openai.api_key = self.api_key
    
    def loading_indicator(self):
        chars = "|/-\\"
        while not self.api_done.is_set():
            for char in chars:
                sys.stdout.write(f"\r{char} {self.name}の応答を待っています...")
                sys.stdout.flush()
                time.sleep(0.1)
                if self.api_done.is_set():
                    break
    
    def call_api(self, user_message):
        self.messages.append({
            "role": "user",
            "content": user_message
        })
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        message = completion["choices"][0]["message"]
        print("\r" + message["content"])
        self.messages.append(message)
        self.api_done.set()
        
    def start_chat(self):
        indicator_thread = threading.Thread(target=self.loading_indicator)
        api_thread = threading.Thread(target=self.call_api, args=("自己紹介と挨拶をしてください。",))
        indicator_thread.start()
        api_thread.start()
        api_thread.join()
        indicator_thread.join()
        while True:
            user_message = input("->")
            self.api_done.clear()
            indicator_thread = threading.Thread(target=self.loading_indicator)
            api_thread = threading.Thread(target=self.call_api, args=(user_message,))
            indicator_thread.start()
            api_thread.start()
            api_thread.join()
            indicator_thread.join()

name = input("成りきってほしい有名人の名前をあげてください：")
print(name + "になりきったbotで対応します。")
chat_bot = ChatBot(name)
chat_bot.start_chat()