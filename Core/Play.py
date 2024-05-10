from pywhatkit import playonyt
import socket


class Player:
    def __init__(self, song):
        if self.has_internet():
            playonyt(song)

    @staticmethod
    def has_internet(self):
        try:
            host = socket.gethostbyname('one.one.one.one')
            s = socket.create_connection((host, 80), 2)
            s.close()

            return True
        except Exception as e:
            print(e)
        return False
