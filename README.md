# Voice Assistant for Personal Computers

## Introduction

Welcome to the Voice Assistant for Personal Computers project! This project aims to create a versatile voice-controlled assistant for personal computers using Python and PyQt6. With the increasing integration of voice recognition technology into various devices, a voice assistant for computers provides a convenient and efficient way to interact with the system hands-free.

The assistant is designed to perform a variety of tasks, ranging from basic commands like opening applications and setting reminders to more complex tasks like fetching information from the web and sending emails. By leveraging the power of natural language processing and machine learning, the assistant can understand and respond to user commands in a human-like manner.

## Features

- **Voice Recognition**: The assistant utilizes speech recognition technology to understand user commands spoken in natural language.
- **Task Automation**: Perform tasks such as opening applications, setting reminders, sending emails, and more, all through voice commands.
- **Customizable**: Easily extend the functionality of the assistant by adding custom commands and actions tailored to your specific needs.
- **Cross-Platform**: Compatible with various operating systems, including Windows, macOS, and Linux, thanks to its Python-based implementation.
- **PyQt6 Interface**: Utilizes PyQt6 to provide a user-friendly graphical interface for interacting with the assistant.
- **Modular Design**: The project is organized into multiple files and modules, making it easy to understand, maintain, and extend.

## Installation

To use the Voice Assistant for Personal Computers, follow these steps:

1. Clone the repository to your local machine:

```
git clone https://github.com/your-username/voice-assistant.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Set up API keys:

   - In the `.env` file, input your own API keys for the respective services:
     ```
     OPENAI_KEY=
     OPEN_WEATHER_KEY=
     PAYSTACK_SECRET_KEY=
     ```

4. Set subscription amount:

   - In the `.env` file, set the subscription amount per month:
     ```
     SUBSCRIPTION_AMOUNT_PER_MONTH=3000
     ```

5. Run the main Python script to start the voice assistant:

```
python app.py
```

## Usage

Once the voice assistant is running, you can interact with it by speaking commands aloud or using the graphical interface provided by PyQt6. Here are some example commands to get you started:

- "Open apps": Opens any application on your computer.
- "Set a reminder": Prompts the assistant to ask for details and sets a reminder based on user input.
- "Send an email": Guides the user through the process of composing and sending an email.
- "What's the weather like today?": Fetches and displays the current weather forecast.
- "Web searches": Some prompts would initiate a web search
- "Arithmetic calculations":  it can perform simple to slightly complex mathematical questions.
  

Feel free to explore the existing commands and add your own custom commands to enhance the functionality of the assistant.

## Project Structure

- **app.py**: The main file to get the voice assistant started.
- **Core**:
  - **Engine.py**: Handles everything regarding processing commands and executing.
  - **Chat.py**: Handles the microphone and text buttons on the interface.
  - **info.py**: Handles what is displayed on the screen.
  - **Setting.py**: Handles everything on the settings page.
- **Services/Payments**:
  - **Paystack**:
    - **Paystack.py**: Initiates the endpoint with Paystack API.
    - **Transaction.py**: Contains things concerning the subscription of the voice assistants.

## Note 
- The speak button is only activated when the subscription is active, so make sure you activate a test subscription to test the STT
  
## Contributing

Contributions to the Voice Assistant for Personal Computers project are welcome! Whether you're interested in adding new features, fixing bugs, or improving documentation, your contributions help make the project better for everyone. To contribute, simply fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



