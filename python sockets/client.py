import time
import socket


class ClientError(Exception):
    pass


class Client:

    def __init__(self, host, port, timeout=None):
        self.socket = socket.create_connection((host, port))
        # self.socket = socket.socket()
        # self.socket.connect((host, port))
      #  self.socket.settimeout(timeout)

    def put(self, key, value, timestamp=int(time.time())):
        put_string = ' '.join(['put', key, str(value), str(timestamp)]) + '\n'
        self.socket.sendall(put_string.encode('utf-8'))

        response = self.socket.recv(1024)
        if not response.startswith('ok'.encode('utf-8')):
            raise ClientError

    def get(self, key):
        get_string = 'get ' + key + '\n'
        response = ''
        self.socket.sendall(get_string.encode('utf-8'))
        while True:
            response += self.socket.recv(1024).decode('utf-8')
            if response.endswith('\n\n'):
                break

        if response == 'ok\n\n':
            return {}
        elif response.startswith('ok'):
            return self.to_dict(response)
        else:
            raise ClientError()

    @staticmethod
    def to_dict(text):
        dict = {}
        text = text[3:-2].split('\n')

        for str in text:
            key, value, timestamp = str.split()
            value = float(value)
            timestamp = int(timestamp)

            if key in dict:
                list_ = dict[key]

                for tuple_ in list_:
                    if tuple_[0] == timestamp:
                        list_.remove(tuple_)
                        break

                list_.append((timestamp, value))
            else:
                dict.update({key: [(timestamp, value)]})

        return dict

    def close(self):
        self.socket.close()
