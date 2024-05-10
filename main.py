import time
import datetime
from tkinter import *



app = Tk()
app.geometry('800x600')
app.title('Voice Assistant')
app.resizable(False, False)
lab = Label(app)
# lab.pack

default_color = '#02182D'
app['bg'] = '#02182D'

# var = StringVar()


# sun_img = Image.open('C:\\Users\\asus\\Documents\\python programming\\VoiceAssistant\\sun.png')
# sun_img = ImageTk.PhotoImage(sun_img)

# Label(app, image=sun_img)

# Handles the greetings: Good morning, Good afternoon etc.
def greeting():

    def greet():
        currentTime = int(time.strftime('%H'))
        if currentTime < 12:
            return "Good Morning"
        elif currentTime < 17:
            return 'Good Afternoon'
        elif currentTime < 21:
            return 'Good Evening'
    app.after(1000, greeting)

    # To display the greetings
    Label(app, text=greet(),
           font =('Poppins', '20'),
           background=default_color,
           fg="#ffffff").place (x=30, y=20)


greeting()


# Handles the time
def clock():
    Time = datetime.datetime.now().strftime("%H:%M %p")
    app.after (1000, clock)  # run itself again after 1000 ms
    # This label is to display the time
    Label (app, text=Time,
           font=('Satoshi', '20'),
           background=default_color,
           fg="#ffffff").place(x=100, y=68, height=25, width=122)

# To display the time
clock()


def action():
    import voiceassistant
    user_Input = voiceassistant.take_command()
    app.after(1000, user_Input)
    # textOutput= print()

    Label(app, text= user_Input,
           font=('Satoshi', '20'),
           background=default_color,
           fg="#ffffff").place(x=300, y=68)

orb_img = PhotoImage(file="C:\\Users\\asus\\Documents\\python programming\\VoiceAssistant\\orb.png")
Button(app, image=orb_img, command=action, borderwidth=0, highlightthickness=0, relief='flat',) \
    .place(x=350, y=400, width=89.5, height=89.5,)


# sun_img = PhotoImage(file='C:\\Users\\asus\\Documents\\python programming\\VoiceAssistant\\sun.png')
# Label(app, image=sun_img).place(x=235,y=36, width=24, height=24)


app.mainloop()
