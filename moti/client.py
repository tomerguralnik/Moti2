import socket
import click
import datetime
from .thought import Thought
from .utils import Connection
from .cli import cli

@cli.command()
@click.option('--address', prompt = 'Adress', help = 'Adress of server')
@click.option('--user', prompt = 'user', help = 'User id of sender')
@click.option('--thougt', prompt = 'thought', help = 'The thought')
def upload_thought(address, user, thought):
    thought = Thought(int(user), datetime.datetime.now(), thought)
    message = thought.serialize()
    address = address.split(':')
    address = (address[0],int(address[1]))
    sender = socket.socket()
    sender.connect(address)
    conn = Connection(sender)
    conn.send(message)
    conn.close()
    print('done')

if __name__ == '__main__':
    cli.main()
