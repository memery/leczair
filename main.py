
import network
import time


def init():
    sock = network.BufferedSocket('127.0.0.1', 6667)
    sock.write('NICK phi-beta')
    sock.write('USER phi-beta 0 * :real phi-beta')
    time.sleep(2)
    sock.write('JOIN #leczair')


if __name__ == '__main__':
    init()


