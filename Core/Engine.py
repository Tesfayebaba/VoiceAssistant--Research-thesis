import sys
from datetime import date, datetime, timedelta
import os
import pyjokes
import pyttsx3
import openai
from random import choice, randrange
import webbrowser
from Core.Play import Player


class Engine:
    def __init__(self, command):
        self.search_words = {
            "who": "who",
            "when": "when",
            "where": "where",
            "why": "why",
            "how": "how",
            "search": "search",
            "find": "find"
        }
        self.Yes_dating_Response = ["I'm sorry, am in love with the internet", "I'm flattered, Thank you.",
                               "I'll add you to the list", "I'm flattered, but how's that going to work?"]

        self.how_are_you = ["I'm fine, thank you.", "Just being busy, being your favourite assistant.",
                       "I'm okay.", "I'm doing well. Thank you.", "I am doing okay."]

        self.talk_dating_response = ["Are you interested in having a relationship with me?",
                                "I'm married to the idea of helping you"]

        self.im_sad_response = [""]

        self.error_phrases = ["Please say that again, i don't seem to get that",
                         "oops!, i don't know how to do that yet",
                         "I'm having difficulty getting that can you say that again?",
                         "I'm having some trouble understanding that can you say that again?"]

        self.age_questions = ["not sure, but i know i get older every minute"]

        # Used to store command logs for future analysis
        self.conversation_log = 'Data/logs.txt'
        self.wake = 'valentine'

        self.command = command


    # Handles all the commands
    def handler(self):
        # log start of conversation
        self.log_conversation('Conversation started')
        command = self.command.lower()

        try:
            if 'play' in command:
                song = command.replace('play', '')
                return {'text': 'Playing ' + song, 'action': 'play', 'data': song}

            elif 'time' in command:
                time = datetime.now().strftime("%H:%M %p")
                return {'text': 'The time is ' + time, 'action': 'talk'}

            elif 'how are you' in command:
                return {'text': choice(self.how_are_you), 'action': 'talk'}

            elif "let's go on a date" in command:
                response = 'sorry, I have a headache. Maybe some other time.'
                return {'text': response, 'action': 'talk'}

            elif "are you single" in command:
                index = randrange(1)
                response = self.talk_dating_response[index]
                return {'text': response, 'action': 'talk'}

            elif 'joke' in command:
                joke = pyjokes.get_joke()
                return {'text': joke, 'action': 'talk'}

            elif self.search_words.get(command.split(' ')[0]) == command.split(' ')[0]:
                response = 'Here is what I found'
                search_query = f"https://google.com/search?q={command}"
                return {'text': response, 'action': 'open', 'data': search_query}

            elif command == 'open youtube':
                response = 'Opening YouTube...'
                return {'text': response, 'action': 'open', 'data': 'https://youtube.com'}

            elif command == 'open instagram':
                response = 'Opening Instagram...'
                return {'text': response, 'action': 'open', 'data': 'https://instagram.com'}

            elif command == 'open google':
                response = 'Opening Google...'
                return {'text': response, 'action': 'open', 'data': 'https://google.com'}

            elif "last week" in command:
                today = date.today()
                datetime.now()
                date_intent = today - timedelta(days=7)
                response = date_intent.strftime("%d-%m-%Y %H:%M:%S")
                return {'text': response, 'action': 'talk'}

            elif "what is your age" in command:
                response = self.age_questions[0]
                response = response
                return {'text': response, 'action': 'talk'}

            elif "what's your age" in command:
                response = self.age_questions[0]
                response = response
                return {'text': response, 'action': 'talk'}

            elif "how old are you" in command:
                response = self.age_questions[0]
                response = response
                return {'text': response, 'action': 'talk'}

            elif "weather" in command:
                pass

            elif "where is" in command:
                pass

            elif command == 'exit':
                sys.exit(1)

            elif command == 'close':
                sys.exit(1)

            elif 'define' in command:
                response = self.chatgpt(command)
                return {'text': response, 'action': 'talk'}

            elif 'explain' in command:
                response = self.chatgpt(command)
                return {'text': response, 'action': 'talk'}

            elif 'describe' in command:
                response = self.chatgpt(command)
                return {'text': response, 'action': 'talk'}

            elif 'calculate' in command:
                response = self.chatgpt(command)
                return {'text': response, 'action': 'talk'}

            elif 'solve' in command:
                response = self.chatgpt(command)
                return {'text': response, 'action': 'talk'}

            elif 'what' in command:
                response = self.chatgpt(command)
                return {'text': response, 'action': 'talk'}

            elif 'how' in command:
                response = self.chatgpt(command)
                return {'text': response, 'action': 'talk'}

            elif 'when' in command:
                response = self.chatgpt(command)
                return {'text': response, 'action': 'talk'}

            elif 'meaning' in command:
                response = self.chatgpt(command)
                return {'text': response, 'action': 'talk'}

            elif 'definition' in command:
                response = self.chatgpt(command)
                return {'text': response, 'action': 'talk'}

            else:
                error = choice(self.error_phrases)
                return {'text': error, 'action': 'talk'}
        except Exception as e:
            print(e)
            error = 'Your request could not be processed.'
            return {'text': error, 'action': 'talk'}

    def talk(self, text):
        engine = pyttsx3.init()
        # male voice
        engine.setProperty('gender', 'male')
        engine.setProperty('rate', 150)

        engine.say(text)
        engine.runAndWait()

    def play(self, song):
        Player(song)

    def open(self, url):
        webbrowser.open(url)

    def log_conversation(self, text):
        today = str(date.today())
        with open(self.conversation_log, 'a') as log_file:
            log_file.write(text + ': ' + today + "\n")
            log_file.close()

    def chatgpt(self, command):
        openai.api_key = os.getenv('OPENAI_KEY')

        engine = 'text-davinci-003'
        completion = openai.Completion.create(
            engine=engine,
            prompt=command,
            max_tokens=1024,
            stop=None,
            top_p=1.0,
            frequency_penalty=0.2,
            presence_penalty=0.0,
            temperature=0
        )

        return completion.choices[0].text
