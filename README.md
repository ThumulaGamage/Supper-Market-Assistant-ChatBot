#  Supermarket Assistant Chatbot

A Natural Language Processing (NLP) powered chatbot designed to help customers locate items in a supermarket environment. This project demonstrates practical application of NLP techniques for real-world problem solving.

##  Overview

The Supermarket Assistant Chatbot uses advanced NLP techniques to understand customer requests and provide accurate shelf locations for requested items. The system features a modern, user-friendly GUI with WhatsApp-style chat interface and comprehensive shopping list management.

## Features

- **Natural Language Understanding**: Uses spaCy NLP library for intelligent text processing
- **Smart Item Recognition**: Extracts items from natural language using tokenization, POS tagging, and named entity recognition
- **Interactive Chat Interface**: WhatsApp-style GUI with message bubbles and timestamps
- **Shopping List Management**: Create, view, and manage shopping lists with categorization
- **Print Functionality**: Export shopping lists to text files
- **Error Handling**: Robust error handling for missing items and system issues
- **Multi-Item Support**: Process multiple items in a single request
- **Fuzzy Matching**: Handles variations in spelling and plural/singular forms

##  Technical Requirements

### Prerequisites
- Python 3.7 or higher
- tkinter (usually comes with Python)
- spaCy NLP library
- spaCy English model

### Required Libraries
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

## Project Structure

```
supermarket-chatbot/
│
├── chatbot_gui.py          # Main application file
├── products.json           # Product database
├── README.md              # This file
├── user_guide.pdf         # Comprehensive user guide
└── requirements.txt       # Python dependencies
```

## Installation & Setup

1. **Clone or download the project files**
   ```bash
   # Ensure you have all project files in the same directory
   ```

2. **Install required dependencies**
   ```bash
   pip install spacy
   python -m spacy download en_core_web_sm
   ```

3. **Verify products.json exists**
   - Ensure `products.json` is in the same directory as `chatbot_gui.py`
   - The file should contain the product database structure

4. **Run the application**
   ```bash
   python chatbot_gui.py
   ```

##  How to Use

### Basic Usage
1. Launch the application by running `chatbot_gui.py`
2. Type your request in the input field (e.g., "I need apples and milk")
3. Press Enter or click Send
4. View the shelf locations in the chat interface

### Sample Queries
- **Single item**: "I need bread"
- **Multiple items**: "I want apples, milk, and chocolate"
- **Natural language**: "Where can I find eggs and bacon for breakfast?"
- **Mixed case**: "I need BANANAS and cheese"

### Shopping List Features
- **View List**: Click " My shopping list to see all requested items
- **Print List**: Click " Export list to save a text file
- **Clear Chat**: Click "New session" to start a new chat

##  Product Database

The system supports 10+ categories with 50+ items:
- Fruits (Shelf 1)
- Dairy Products (Shelf 2)
- Bakery Items (Shelf 3)
- stationary (Shelf 4)
- Cleaning Supplies (Shelf 5)
- Beverages (Shelf 6)
- Snacks & Sweets (Shelf 7)
- Frozen Foods (Shelf 8)
- vegetables (Shelf 9)
- Spices & Condiments (Shelf 10)


##  Configuration

### Adding New Items
Edit `products.json` to add new items or categories:
```json
{
  "new_category": {
    "shelf": "Shelf 11 - New Category",
    "items": ["item1", "item2", "item3"]
  }
}
```

### Customizing the Interface
- Modify colors, fonts, and styling in the `create_widgets()` method
- Adjust window size in the `__init__()` method
- Customize greeting messages in the `initial_greeting()` method

##  NLP Techniques Used

- **Tokenization**: Breaking text into individual words/tokens
- **Part-of-Speech Tagging**: Identifying nouns and proper nouns
- **Lemmatization**: Converting words to their base form
- **Named Entity Recognition**: Extracting meaningful entities
- **Fuzzy Matching**: Handling spelling variations and plural forms

## Troubleshooting

### Common Issues

**"spaCy model not found" error:**
```bash
python -m spacy download en_core_web_sm
```

**"products.json file not found" error:**
- Ensure `products.json` is in the same directory as `chatbot_gui.py`
- Check file permissions

**GUI not displaying properly:**
- Ensure tkinter is installed (comes with most Python installations)
- Try running on Python 3.7+

##  Performance

- **Response Time**: Typically under 1 second for item lookup
- **Memory Usage**: Approximately 50-100 MB
- **Supported Items**: 50+ predefined items, easily expandable
- **Concurrent Queries**: Handles multiple items in single request

##  Educational Value

This project demonstrates:
- Practical NLP application development
- GUI programming with tkinter
- JSON data management
- Object-oriented programming principles
- Error handling and user experience design
- Integration of multiple Python libraries

##  Assignment Compliance

**Functional Requirements:**
-  Customer can input list of goods
-  NLP extraction of items from input
-  Database search and shelf location response
-  Display and print item lists
-  Handles 10+ different goods

**Technical Requirements:**
-  Uses spaCy NLP library
-  GUI-based user interface
-  Proper NLP techniques implementation

##  Author

Created for CO3251 - Natural Language Processing | Assignment 2

For detailed usage instructions, please refer to the User Guide document included in this project.