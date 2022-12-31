from socket import *
from cryptography.fernet import Fernet
import base64


class Client:
    def __init__(self, ip, port):
        self.cli = socket(AF_INET, SOCK_STREAM)
        self.cli.connect(
            (ip, port)
        )

        symbols = {
            '0': 'Q', '1': 'W', '2': 'E', '3': 'R', '4': 'T', '5': 'Y', '6': 'U', '7': 'I', '8': 'O', '9': 'P',
        }
        p = self.cli.getsockname()[0].replace('.', '')
        i = 0
        key = ''
        while len(key) != 32:
            key = f'{key}{symbols[p[i]]}'
            i += 1
            if i == len(p):
                i = 0
        key = key.encode()
        key = base64.urlsafe_b64encode(key)
        self.f = Fernet(key)

        self.connected = False

        self.client_return = []

    def sender(self, text):
        text = str(text).encode()
        text = self.f.encrypt(text)
        try:
            self.cli.send(text)
        except Exception as e:
            pass

    def get_msg(self):
        data = self.cli.recv(1024)
        data = self.f.decrypt(data)
        msg = data.decode()
        return msg

    def connect(self):
        self.connected = True
        msg = self.get_msg()
        print(msg)

    def listen(self, answer):
        data = str(answer)
        if not (data in ('disconnect', 'exit')):
            try:
                self.sender(data)
                msg = self.get_msg()
            except Exception as e:
                print(e)
                print('Server disconnected!')
                msg = 'Server disconnected!'

            if msg != 'default switch':
                if msg == 'Server disconnected!':
                    exit()

                else:
                    msg = eval(msg)
                    self.client_return = msg

        else:
            self.sender('disconnect')
            self.cli.close()
            print('Exiting...')
            exit()


if __name__ == '__main__':
    app = Client('26.17.241.162', 7000)
    app.connect()
