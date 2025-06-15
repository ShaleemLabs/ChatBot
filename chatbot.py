import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import ollama
import csv
from datetime import datetime

# Constants for the model and initial personality selection
MODEL_NAME = "gemma3:1b"
SELECTED_PERSONALITY = {"key": "Chill"}  # Default selected personality
CHAT_HISTORY = []  # Stores chat messages along with metadata


def main():
    """
    Initializes the main Tkinter window, creates layout frames,
    loads previous chat history, and starts the event loop.
    """
    root = tk.Tk()
    root.geometry("800x500")
    root.title("ChatBot")

    # Create main layout frames: top, chat display, input, and buttons
    frames = {}
    for name in ['top', 'chat', 'input', 'button']:
        frames[name] = tk.Frame(root)
        frames[name].pack(padx=3, pady=3, fill=tk.BOTH, expand=True)

    # Assign references to frames
    top_frame = frames['top']
    chat_frame = frames['chat']
    input_frame = frames['input']
    button_frame = frames['button']

    # Build GUI components
    create_top_frame(top_frame, on_personality_selected)
    chat = create_chat_frame(chat_frame)
    user_input = create_input_frame(input_frame)
    create_button_frame(button_frame, chat, user_input)

    # Attempt to load previous chat history
    error_message = load_chat_history(chat)
    if error_message:
        messagebox.showerror("Load Error", error_message)

    root.mainloop()


def create_top_frame(frame, on_personality_selected):
    """
    Creates the top frame UI with a label and a combobox
    to allow user to select a chatbot personality.
    """
    frame.columnconfigure(0, weight=1)

    top_label = tk.Label(frame, text="Choose Personality!", font=("Comic Sans", 16, "bold"))
    top_label.grid(row=0, column=0, padx=10)

    persona_selector = ttk.Combobox(
        frame,
        values=list(system_personas().keys()),
        state="readonly",
        font=("Comic Sans", 10)
    )
    persona_selector.grid(row=1, column=0, padx=10)
    persona_selector.set(SELECTED_PERSONALITY['key'])  # Set default personality

    # Update selected personality on user selection
    def update_personality(event):
        on_personality_selected(persona_selector.get())

    persona_selector.bind("<<ComboboxSelected>>", update_personality)


def create_chat_frame(frame):
    """
    Creates a read-only chat display area with scroll functionality.
    """
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    chat_display = scrolledtext.ScrolledText(
        frame,
        wrap='word',
        state='disabled',
        height=20
    )
    chat_display.grid(row=0, column=0, sticky='nsew', padx=10)

    return chat_display


def create_input_frame(frame):
    """
    Creates an input field where the user types their message.
    """
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    user_input = tk.Entry(frame)
    user_input.grid(row=0, column=0, sticky='ew', padx=10)
    return user_input


def create_button_frame(frame, chat, user_input):
    """
    Creates three buttons: Send, Save, and Clear.
    Binds them to their respective functionality.
    Also binds Enter key to send the message.
    """
    for row in range(3):
        frame.rowconfigure(row, weight=1)
    frame.columnconfigure(0, weight=1)

    # --- Send Message Button ---
    send_button = tk.Button(frame, text="Send Message")
    send_button.grid(row=0, column=0, sticky='ew', padx=10)

    def send_message():
        """
        Sends user message, fetches bot reply, displays both,
        and appends them to the chat history.
        """
        message = user_input.get().strip()
        if message:
            chat.config(state="normal")
            chat.insert(tk.END, f"You: {message}\n")
            user_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            CHAT_HISTORY.append({"Role": "You", "Message": message, "TimeStamp": user_timestamp})

            # Get bot response based on selected personality
            response = generate_responses(message, SELECTED_PERSONALITY['key'])
            chat.insert(tk.END, f"{SELECTED_PERSONALITY['key']}Bot: {response}\n\n")
            bot_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            CHAT_HISTORY.append({"Role": f"{SELECTED_PERSONALITY['key']}Bot", "Message": response, "TimeStamp": bot_timestamp})

            chat.config(state="disabled")
            chat.yview(tk.END)
            user_input.delete(0, tk.END)

    send_button.config(command=send_message)

    # --- Save Chat Button ---
    save_button = tk.Button(frame, text="Save Chat")
    save_button.grid(row=1, column=0, sticky='ew', padx=10)

    def save_chat():
        """
        Saves the current chat history to a CSV file.
        """
        if CHAT_HISTORY:
            error_message = save_chat_history()
            if error_message:
                messagebox.showerror("Save Error", error_message)
            else:
                messagebox.showinfo("Success", "Chat saved successfully!")

    save_button.config(command=save_chat)

    # --- Clear Chat Button ---
    clear_button = tk.Button(frame, text="Clear Chat")
    clear_button.grid(row=2, column=0, sticky='ew', padx=10)

    def clear_chat(chat, history):
        """
        Clears the chat display and history.
        """
        chat.config(state='normal')
        chat.delete("1.0", tk.END)
        chat.config(state='disabled')
        history.clear()

    clear_button.config(command=lambda: clear_chat(chat, CHAT_HISTORY))

    # --- Bind Enter Key to Send ---
    user_input.bind("<Return>", lambda event: send_button.invoke())
    user_input.focus_set()


def system_personas():
    """
    Defines the available chatbot personalities.
    """
    return {
        "Chill": "You're a relaxed chatbot that keeps things casual and light.",
        "Sarcastic": "You are a sarcastic chatbot, who cares for the user but hides it under the hood. Be brief with your responses.",
        "Formal": "You are a formal and sophisticated chatbot, catering to user's demands. Use zero filler words."
    }


def on_personality_selected(new_personality):
    """
    Updates the currently selected personality when the user selects one.
    """
    SELECTED_PERSONALITY["key"] = new_personality


def generate_responses(prompt, personality_key):
    """
    Uses Ollama API to generate a chatbot response based on the selected personality.
    Returns the content or an appropriate error message.
    """
    try:
        personalities = system_personas()
        responses = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": personalities[personality_key]},
                {"role": "user", "content": prompt}
            ]
        )
        return responses["message"]["content"].strip()
    except KeyError:
        return "Oops! I couldn't understand the model's reply. Let's try again."
    except Exception as e:
        return f"Sorry, something went wrong while trying to reply. (Details: {e})"


def save_chat_history(filename="chat_history.csv"):
    """
    Saves the chat history list to a CSV file.
    If file doesn't exist, headers are added.
    Returns error message if saving fails.
    """
    fieldnames = ["Role", "Message", "TimeStamp"]
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write header only if file is empty
            file.seek(0, 2)  # Go to end of file
            if file.tell() == 0:
                writer.writeheader()

            for entry in CHAT_HISTORY:
                writer.writerow(entry)
    except PermissionError:
        return "Failed to save chat history. You may not have permission."
    except FileNotFoundError:
        return "Failed to save chat history. File not found."
    except Exception as e:
        return f"Failed to save chat history. (Details: {e})"
    return None


def load_chat_history(chat_widget, filename="chat_history.csv"):
    """
    Loads chat history from CSV into the chat display widget.
    Updates CHAT_HISTORY list. Returns error message on failure.
    """
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            chat_widget.config(state="normal")

            for row in reader:
                role = row["Role"]
                message = row["Message"]
                timestamp = row["TimeStamp"]
                chat_widget.insert(tk.END, f"{role}: {message}\n")
                CHAT_HISTORY.append({"Role": role, "Message": message, "TimeStamp": timestamp})

            chat_widget.config(state="disabled")
            chat_widget.yview(tk.END)
    except FileNotFoundError:
        # File not found is not treated as an error
        return None
    except Exception as e:
        return f"Failed to load chat history.\n\nDetails:\n{e}"
    return None


# Entry point for the program
if __name__ == "__main__":
    main()
