# NUVEXA AI

**Your Living AI Assistant with Execution Power**

## What is NUVEXA?

NUVEXA is not another chatbot. It's a living AI assistant that completes tasks for you, including AI-native shopping and checkout. Built with modern Python best practices, type safety, and robust error handling.

## Features

- 🤖 **Assistant Mode**: General help, planning, and research
- 🛒 **Shopping Mode**: Intelligent product search and seamless checkout
- 💭 **Therapist Mode**: Emotional support and active listening
- 🏗️ **Builder Mode**: Project planning and visual simulation

### Enhanced Features

- ✅ **Smart Cart Management**: Add, remove, and update quantities
- ✅ **Order History**: Track your past purchases
- ✅ **Improved Search**: Better product discovery with keyword matching
- ✅ **Persistent Settings**: Avatar preferences saved across sessions
- ✅ **Error Handling**: Graceful error messages and recovery
- ✅ **Modern API**: Uses latest OpenAI client library
- ✅ **Type Safety**: Full type hints for better code quality
- ✅ **Database Optimization**: Indexed queries for better performance

## Quick Start

1. Run **SETUP.bat** to install dependencies
2. Edit **.env** file and add your OpenAI API key
3. Run **RUN_NUVEXA.bat** to start
4. NUVEXA opens in your browser!

## Requirements

- Windows 10/11
- Python 3.8 or higher
- OpenAI API key (get one at: https://platform.openai.com/api-keys)

## Project Structure

```
NUVEX12526/
├── app.py              # Main Streamlit application
├── assistant.py        # AI assistant with mode switching
├── shopping.py         # Product search engine
├── database.py         # SQLite database handler
├── config.py           # Configuration and constants
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (API keys)
├── SETUP.bat          # Setup script
└── RUN_NUVEXA.bat     # Run script
```

## Usage Tips

### Shopping Mode
- Say "I want to buy [product]" or "Find me [product]"
- Browse results and add items to cart
- Manage quantities and remove items before checkout
- View order history in the sidebar

### Assistant Mode
- Ask questions, get help with planning
- Research topics and get actionable advice

### Therapist Mode
- Share your thoughts and feelings
- Get empathetic support and guidance

### Builder Mode
- Plan projects step-by-step
- Get recommendations for parts and materials

## Technical Improvements

This version includes significant improvements:

- **Modern OpenAI API**: Migrated from deprecated `openai.api_key` to `OpenAI()` client
- **Type Hints**: Full type annotations for better IDE support and code clarity
- **Error Handling**: Comprehensive try-catch blocks with user-friendly messages
- **Database**: Context managers for safe database operations, proper indexing
- **Code Quality**: Logging, input validation, and documentation
- **UI Enhancements**: Better styling, loading states, and user feedback

## The NUVEXA Vision

Traditional AI tools give you answers but leave you to execute manually. NUVEXA completes the follow-through - turning intention into action.

Built with ❤️ to solve the AI execution gap.

## License

Free to use and modify for personal projects.
