import threading
from pathlib import Path
from struct import *
import click
from .cli import cli
from .utils import Connection
from .utils import Listener
from .thought import Thought

@cli.command()
@click.option('--address', prompt = 'Adress', help = 'Adress of server')
@click.option('--data', prompt = 'data dict', help = 'The path to data dictionary')
def run_server(address, data):
    address = address.split(':')
    host, port = address[0],int(address[1])
    server = Listener(port, host)
    server.start()
    p = Path(data)
    if p.is_file():
        raise Exception('path is a file and not a directory')
    while True:
        client = server.accept()
        t = threading.Thread(target = recieve_message,args = (client, p))
        t.start()
    server.stop()

def recieve_message(client, path):
    l = threading.Lock()
    message = b''
    try:
        header = client.receive(20)
    except Exception as e:
        print(e)
        print('bad header')
        return
    thought_len = unpack('I', header[16:])[0]
    try:
        thought = client.receive(thought_len)
    except:
        print('thought too short')
        return
    message = header + thought
    thought = Thought.deserialize(message)
    l.acquire()
    p = path / str(thought.user_id)
    p.mkdir(exist_ok = True, parents = True)
    t = thought.timestamp.strftime('%Y-%m-%d_%H-%M-%S') + '.txt'
    p = p / t
    if(p.exists()):
        f = p.open(mode = 'a+')
        f.write('\n'+str(thought))
    else:
        p.touch()
        f = p.open(mode = 'a+')
        f.write(str(thought))
    f.close()
    l.release()

if __name__ == '__main__':
    cli.main()
