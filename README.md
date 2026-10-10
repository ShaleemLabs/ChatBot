# AI ChatBot with Custom Personalities

A Python desktop chatbot built with Tkinter and powered by a locally running Ollama language model. The application allows users to interact with an AI chatbot through three distinct personalities: Chill, Sarcastic, and Formal.

It also supports saving and restoring conversations through CSV files, providing a simple way to preserve chat history between sessions.

## Features

- **Three chatbot personalities:** Choose between Chill, Sarcastic, and Formal response styles.
- **Local AI integration:** Uses Ollama to generate responses with the `gemma3:1b` model.
- **Desktop graphical interface:** Built with Python's Tkinter and ttk libraries.
- **Persistent chat history:** Loads previously saved conversations when the application starts.
- **CSV export:** Saves conversations with the speaker, message, and timestamp.
- **Keyboard shortcuts:** Press Enter to send a message.
- **Conversation management:** Clear the current conversation and its in-memory history.
- **Scrollable chat display:** View messages in a dedicated scrolling text area.

## Technologies Used

- **Python** — Core application logic
- **Tkinter / ttk** — Desktop graphical user interface
- **Ollama** — Local AI response generation
- **CSV** — Conversation history storage
- **Datetime** — Message timestamps

## Requirements

- Python 3.10 or later recommended
- [Ollama](https://ollama.com/) installed and running locally
- The `gemma3:1b` model downloaded
- The Python `ollama` package

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

Replace the placeholders with your actual GitHub repository URL and directory name.

### 2. Install Ollama

Download and install Ollama:

https://ollama.com/download

Download the model used by the application:

```bash
ollama pull gemma3:1b
```

Make sure Ollama is running before starting the chatbot.

### 3. Install the Python dependency

```bash
python -m pip install ollama
```

Tkinter is included with many standard Python installations. On some Linux distributions, it may need to be installed separately.

### 4. Run the application

Run the Python script containing the application:

```bash
python chatbot.py
```

Replace `chatbot.py` with the actual filename if it differs.

## How to Use

1. **Launch the application.** The chatbot window opens with Chill selected by default.
2. **Choose a personality.** Use the dropdown menu to switch between Chill, Sarcastic, and Formal.
3. **Enter a message.** Type your message into the input field.
4. **Send the message.** Click **Send Message** or press Enter.
5. **Save your conversation.** Click **Save Chat** to append the current in-memory conversation history to a CSV file.
6. **Clear the conversation.** Click **Clear Chat** to remove the displayed messages and clear the in-memory history.

## Chatbot Personalities

| Personality | Description |
|---|---|
| Chill | Relaxed, casual, and lighthearted |
| Sarcastic | Brief, sarcastic, and caring beneath the surface |
| Formal | Sophisticated, direct, and professional |

Each personality is implemented through a system prompt sent to the local Ollama model.

## Chat History

The application uses a CSV file named:

```text
chat_history.csv
```

Each record contains three fields:

| Field | Description |
|---|---|
| Role | The speaker, such as You or ChillBot |
| Message | The conversation message |
| TimeStamp | The date and time the message was recorded |

The application attempts to load this file at startup. If the file does not exist, the chatbot starts with an empty conversation.

When saving, the application appends the current in-memory history to the CSV file rather than replacing its contents.

**Note:** Because the application appends the entire in-memory history each time you save, previously saved messages can be duplicated in the CSV. Clearing the chat also clears the in-memory history, but it does not delete the existing CSV file.

## Privacy

The chatbot sends prompts to an Ollama instance running locally on your computer instead of using a cloud AI API directly. Conversation history is stored in a local CSV file.

Keep in mind that local AI software and saved conversation files still require appropriate security practices, particularly when handling sensitive information.

## Current Limitations

- Only one language model is configured by default.
- The application does not maintain the full conversation as model context. Each response is generated using the current user message and the selected personality prompt.
- Switching personalities affects subsequent responses but does not change previously generated messages.
- The application does not provide separate conversation sessions or automatic conversation titles.
- AI response quality depends on the selected model and its capabilities.

## Project Purpose

This project explores desktop GUI development, local AI integration, prompt engineering, and CSV-based data persistence. It demonstrates how a locally running language model can be combined with a simple Python interface to create a customizable chatbot without requiring a cloud AI API.

## License

No license has been specified yet. Unless a license is added to this repository, the project should be treated as having all rights reserved by its author.
