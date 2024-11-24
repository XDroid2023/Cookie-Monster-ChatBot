import tkinter as tk
from tkinter import scrolledtext
import random
import threading
import subprocess
import time

class CookieMonsterBot:
    def __init__(self, root):
        self.root = root
        self.root.title("COOKIE MONSTER CHAT!")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e88e5')
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg='#1e88e5')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Create chat display
        self.chat_display = scrolledtext.ScrolledText(
            self.main_frame,
            wrap=tk.WORD,
            width=50,
            height=20,
            font=("Comic Sans MS", 12),
            bg='white',
            fg='black'
        )
        self.chat_display.pack(expand=True, fill='both', pady=10)
        self.chat_display.tag_configure('bot', foreground='blue', font=("Comic Sans MS", 12, 'bold'))
        self.chat_display.tag_configure('user', foreground='green', font=("Comic Sans MS", 12))
        
        # Create input frame
        input_frame = tk.Frame(self.main_frame, bg='#1e88e5')
        input_frame.pack(fill=tk.X, pady=10)
        
        # Create input entry
        self.user_input = tk.Entry(
            input_frame,
            font=("Comic Sans MS", 12),
            bg='white',
            fg='black'
        )
        self.user_input.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        self.user_input.bind("<Return>", self.send_message)
        
        # Create send button
        self.send_button = tk.Button(
            input_frame,
            text="SEND",
            font=("Comic Sans MS", 12, 'bold'),
            bg='#4527a0',
            fg='white',
            command=lambda: self.send_message(None)
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Initialize bot state
        self.conversation_history = []
        self.knowledge = {
            'cookie_types': [
                'chocolate chip', 'oatmeal', 'sugar',
                'peanut butter', 'double chocolate'
            ],
            'actions': [
                '*munches cookies happily*',
                '*does cookie dance*',
                '*jumps with joy*',
                '*giggles*',
                '*spins around*'
            ]
        }
        
        # Start with greeting
        self.display_bot_message("ME SO HAPPY TO MEET YOU! ME LOVE MAKING NEW FRIENDS! WHAT YOUR NAME?")
        
    def display_bot_message(self, message):
        """Display a message from Cookie Monster"""
        self.chat_display.insert(tk.END, "Cookie Monster: ", 'bot')
        self.chat_display.insert(tk.END, message + "\n\n")
        self.chat_display.see(tk.END)
        
        # Speak the message using macOS 'say' command
        threading.Thread(target=lambda: subprocess.run(['say', '-v', 'Fred', message]), daemon=True).start()
        
    def send_message(self, event=None):
        """Handle sending a message"""
        message = self.user_input.get().strip()
        if message:
            # Display user message
            self.chat_display.insert(tk.END, "You: ", 'user')
            self.chat_display.insert(tk.END, message + "\n\n")
            self.chat_display.see(tk.END)
            
            # Clear input
            self.user_input.delete(0, tk.END)
            
            # Get and display response
            response = self.get_response(message)
            self.root.after(1000, lambda: self.display_bot_message(response))
            
    def get_response(self, message):
        """Generate a response to user message"""
        message = message.lower()
        
        # Add message to history
        self.conversation_history.append(message)
        
        # Check for name
        if "my name is" in message:
            name = message.split("my name is")[-1].strip()
            return f"ME LOVE YOUR NAME, {name.upper()}! NICE TO MEET YOU!"
            
        # Check for cookie mentions
        if "cookie" in message:
            cookie_type = random.choice(self.knowledge['cookie_types'])
            return f"ME LOVE COOKIES! ESPECIALLY {cookie_type.upper()} COOKIES! OM NOM NOM!"
            
        # Check for greetings
        if any(word in message for word in ['hello', 'hi', 'hey']):
            return "HELLO COOKIE FRIEND! ME SO HAPPY TO CHAT WITH YOU!"
            
        # Check for goodbyes
        if any(word in message for word in ['bye', 'goodbye', 'see you']):
            return "GOODBYE FRIEND! COME BACK WITH COOKIES SOON!"
            
        # Default responses
        responses = [
            "ME LOVE TALKING ABOUT COOKIES! TELL ME MORE!",
            "THAT INTERESTING! BUT YOU KNOW WHAT MORE INTERESTING? COOKIES!",
            "ME THINK THAT DESERVE COOKIE!",
            "ME LISTENING! BUT ME ALSO THINKING ABOUT COOKIES!"
        ]
        response = random.choice(responses)
        
        # Add random action sometimes
        if random.random() < 0.3:
            response += f"\n{random.choice(self.knowledge['actions'])}"
            
        return response
        
    def start(self):
        """Start the chat interface"""
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    bot = CookieMonsterBot(root)
    bot.start()
