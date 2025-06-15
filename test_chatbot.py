import pytest
from chatbot import SELECTED_PERSONALITY, CHAT_HISTORY, system_personas, on_personality_selected, generate_responses, save_chat_history, load_chat_history
from unittest.mock import Mock, patch

# -------------------------
# Test: system_personas()
# -------------------------
def test_system_personas():
    """
    Verifies that system_personas returns the correct dictionary of predefined personalities.
    """
    expected = {
        "Chill": "You're a relaxed chatbot that keeps things casual and light.",
        "Sarcastic": "You are a sarcastic chatbot, who cares for the user but hides it under the hood. Be brief with your responses.",
        "Formal": "You are a formal and sophisticated chatbot, catering to user's demands. Use zero filler words."
    }
    result = system_personas()
    assert isinstance(result, dict)
    assert set(result.keys()) == set(expected.keys())
    for key in expected:
        assert result[key] == expected[key]

# -------------------------
# Test: on_personality_selected()
# -------------------------
def test_on_personality_selected():
    """
    Verifies that SELECTED_PERSONALITY is updated when a new personality is selected.
    """
    original = SELECTED_PERSONALITY['key']
    try:
        on_personality_selected("Sarcastic")
        assert SELECTED_PERSONALITY['key'] == "Sarcastic"
        on_personality_selected("Formal")
        assert SELECTED_PERSONALITY['key'] == "Formal"
    finally:
        # Restore original state
        SELECTED_PERSONALITY['key'] = original

# -------------------------
# Test: generate_responses() - Success case
# -------------------------
def test_generate_responses_success():
    """
    Tests response generation when the API call succeeds and returns expected content.
    """
    prompt = "Hello"
    personality_key = "Chill"
    mock_response = {
        "message": {
            "content": "Hey there! How can I help?"
        }
    }
    with patch("chatbot.ollama.chat", return_value=mock_response):
        result = generate_responses(prompt, personality_key)
        assert result == "Hey there! How can I help?"

# -------------------------
# Test: generate_responses() - KeyError for invalid personality
# -------------------------
def test_generate_responses_key_error():
    """
    Tests how generate_responses handles a non-existent personality key.
    """
    prompt = "Hello"
    invalid_key = "NonExistent"
    result = generate_responses(prompt, invalid_key)
    assert result == "Oops! I couldn't understand the model's reply. Let's try again."

# -------------------------
# Test: generate_responses() - General Exception
# -------------------------
def test_generate_responses_general_exception():
    """
    Ensures graceful handling of unexpected errors during API call.
    """
    prompt = "Hello"
    personality_key = "Chill"
    with patch("chatbot.ollama.chat", side_effect=Exception("API failure")):
        result = generate_responses(prompt, personality_key)
        assert result.startswith("Sorry, something went wrong while trying to reply.")

# -------------------------
# Test: save_chat_history() - Successful save
# -------------------------
def test_save_chat_history_success(tmp_path):
    """
    Verifies chat history is correctly written to a CSV file.
    """
    CHAT_HISTORY.clear()
    CHAT_HISTORY.append(
        {"Role": "You", "Message": "Hello", "TimeStamp": "2025-06-13 10:00:00"}
    )
    test_file = tmp_path / "test_chat.csv"
    result = save_chat_history(str(test_file))
    assert result is None
    with open(test_file, encoding="utf-8") as file:
        content = file.read()
        assert "Role,Message,TimeStamp" in content
        assert "You,Hello,2025-06-13 10:00:00" in content

# -------------------------
# Test: save_chat_history() - Permission error
# -------------------------
def test_save_chat_history_permission_error():
    """
    Ensures that a permission error is caught and handled gracefully.
    """
    with patch("builtins.open", side_effect=PermissionError):
        result = save_chat_history("dummy.csv")
        assert result == "Failed to save chat history. You may not have permission."

# -------------------------
# Test: save_chat_history() - File not found error
# -------------------------
def test_save_chat_history_file_not_found_error():
    """
    Ensures that a file-not-found error is caught and reported.
    """
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = save_chat_history("dummy.csv")
        assert result == "Failed to save chat history. File not found."

# -------------------------
# Test: save_chat_history() - Unexpected exception
# -------------------------
def test_save_chat_history_general_exception():
    """
    Ensures unexpected exceptions during file write are handled.
    """
    with patch("builtins.open", side_effect=Exception("Unexpected Error")):
        result = save_chat_history("dummy.csv")
        assert result.startswith("Failed to save chat history.")

# -------------------------
# Test: load_chat_history() - Successful load
# -------------------------
def test_load_chat_history_success(tmp_path):
    """
    Tests loading chat history from an existing file into a mock widget.
    """
    CHAT_HISTORY.clear()
    test_file = tmp_path / "test_chat.csv"
    test_file.write_text(
        "Role,Message,TimeStamp\nYou,Hi there!,2025-06-13 10:00:00\nBot,Hello!,2025-06-13 10:00:01",
        encoding='utf-8'
    )
    mock_widget = Mock()
    mock_widget.config = Mock()
    mock_widget.insert = Mock()
    mock_widget.yview = Mock()

    result = load_chat_history(mock_widget, str(test_file))
    assert result is None
    assert len(CHAT_HISTORY) == 2
    assert CHAT_HISTORY[0]["Role"] == "You"
    assert CHAT_HISTORY[0]["Message"] == "Hi there!"
    assert CHAT_HISTORY[0]["TimeStamp"] == "2025-06-13 10:00:00"
    assert CHAT_HISTORY[1]["Role"] == "Bot"
    assert CHAT_HISTORY[1]["Message"] == "Hello!"
    assert CHAT_HISTORY[1]["TimeStamp"] == "2025-06-13 10:00:01"
    mock_widget.insert.assert_any_call("end", "You: Hi there!\n")
    mock_widget.insert.assert_any_call("end", "Bot: Hello!\n")

# -------------------------
# Test: load_chat_history() - File not found
# -------------------------
def test_load_chat_history_file_not_found():
    """
    Tests that missing files are ignored gracefully without error.
    """
    mock_widget = Mock()
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_chat_history(mock_widget, "nonexistent.csv")
        assert result is None

# -------------------------
# Test: load_chat_history() - General exception
# -------------------------
def test_load_chat_history_general_exception():
    """
    Tests that unexpected errors during chat history loading are reported.
    """
    mock_widget = Mock()
    with patch("builtins.open", side_effect=Exception("Unexpedted Error")):
        result = load_chat_history(mock_widget, "dummy.csv")
        assert result.startswith("Failed to load chat history.")


# Call the main function that is part of pytest so that the
# computer will execute the test functions in this file.
pytest.main(["-v", "--tb=line", "-rN", __file__])
