import asyncio


class ClientServerProtocol(asyncio.Protocol):

    database = {}

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def process_data(self, data):
        if data.startswith('put') and data.endswith('\n'):
            self.process_put(data[4:-1])
            return 'ok\n\n'
        elif data.startswith('get') and data.endswith('\n'):
            return self.process_get(data[4:-1])
        else:
            return 'error\nwrong command\n\n'

    def process_put(self, text):
        key, value, timestamp = text.split(' ')
        value = float(value)
        timestamp = int(timestamp)

        if key in self.database:
            list_ = self.database[key]
            for tuple_ in list_:
                if tuple_[0] == timestamp:
                    list_.remove(tuple_)
                    break
            list_.append((timestamp, value))
        else:
            self.database.update({key: [(timestamp, value)]})

    def process_get(self, key):
        response = 'ok\n'

        if key == '*':
            for element in self.database:
                for tuple_ in self.database[element]:
                    response += element + ' ' \
                                + str(tuple_[1]) + ' ' + str(tuple_[0]) + '\n'

        elif key in self.database:
            for tuple_ in self.database[key]:
                response += key + ' ' \
                            + str(tuple_[1]) + ' ' + str(tuple_[0]) + '\n'

        response += '\n'
        return response


def run_server(host, port):

    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


# if __name__ == '__main__':
#     run_server('127.0.0.1', 8888)
