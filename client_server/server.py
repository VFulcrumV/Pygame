from socket import *
from threading import Thread
from cryptography.fernet import Fernet
import base64


class User:
    def __init__(self, ip):
        self.ip = ip
        symbols = {
            '0': 'Q', '1': 'W', '2': 'E', '3': 'R', '4': 'T', '5': 'Y', '6': 'U', '7': 'I', '8': 'O', '9': 'P',
        }
        p = ip.replace('.', '')
        i = 0
        key = ''
        while len(key) != 32:
            key = f'{key}{symbols[p[i]]}'
            i += 1
            if i == len(p):
                i = 0
        key = key.encode()
        self.key = base64.urlsafe_b64encode(key)


class Server:
    def __init__(self, ip, port):
        self.ser = socket(AF_INET, SOCK_STREAM)
        self.ser.bind((ip, port))
        self.ser.listen(5)

        self.blocked = []
        self.users = []
        self.client_return = []

    def get_user(self, ip):
        for user in self.users:
            if user.ip == ip:
                return user
        return None

    def sender(self, user, key, text):
        f = Fernet(key)
        try:
            text = text.encode()
            user.send(f.encrypt(text))
        except Exception as e:
            print('Client disconnected!')

    def get_msg(self, user, key):
        data = user.recv(1024)
        f = Fernet(key)
        data = f.decrypt(data)
        return data.decode()

    def auth(self, user, addr):
        this_user = self.get_user(addr[0])

        if this_user is None:
            self.users.append(User(addr[0]))
            this_user = self.get_user(addr[0])

        print(f'Client is connected: {addr[0]}')
        self.sender(user, this_user.key, 'Connected!')
        self.listen(user, addr)

    def start_server(self):
        while True:
            user, addr = self.ser.accept()
            Thread(target=self.auth, args=(user, addr,)).start()

    def listen(self, user, addr):
        is_work = True
        while is_work:
            try:
                this_user = self.get_user(addr[0])
                msg = self.get_msg(user, this_user.key)
            except Exception as e:
                print('Client disconnected!')
                msg = ''
                is_work = False

            if len(msg) > 0:
                try:
                    data = eval(msg)
                except Exception:
                    data = msg

                if data in ('disconnect', 'exit'):
                    print('Client disconnected!')
                    user.close()
                    is_work = False

                else:
                    this_user = self.get_user(addr[0])
                    if this_user:
                        self.client_return.append(data)
                        answer = str(self.client_return)
                        self.sender(user, this_user.key, answer)
                        self.client_return = []

                    else:
                        user.close()
                        print('Client disconnected!')
                        is_work = False

            else:
                user.close()
                print('Client disconnected!')
                is_work = False


if __name__ == '__main__':
    app = Server('26.17.241.162', 7000)
    app.start_server()
