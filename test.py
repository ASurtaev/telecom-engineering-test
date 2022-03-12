import socket

import settings

TEST_MSGS =[b'1234-04-12:34:59.123-55\r',
            b'7652-04-12:35:01.431-00\r',
            b'0001-04-13:24:34.234-00\r',

            b'',
            b'asd',
            b'001-04-13:24:34.234-00\r',
            b'0001-04-13:224:34.234-00\r',
            b'0001-04-13.24:34.2334-00\r',
            b'0001-04-13:24:34:234-00\r',
            b'0001-04:13:24:34.234-00\r',
            b'0001-13:24:34.234-00\r'
            ]


def run_test():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((settings.test_host, settings.test_port))
        for msg in TEST_MSGS:
            sock.send(msg)
    for msg in TEST_MSGS:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((settings.test_host, settings.test_port))
            sock.send(msg)

if __name__ == '__main__':
    run_test()