import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8001))
sock.listen(5)
while True:
    connection,address = sock.accept()
    try:
        connection.settimeout(5)
        buf = connection.recv(1024)
        print '|'+buf+'|'
        # if buf == '1':
        #     connection.send('welcome to server!')
        # else:
        #     connection.send('please go out!')
        stdin = 'null'
        while stdin != 'end':
            stdin = input('Enter Content')
            connection.send(stdin)
            buf = connection.recv(1024)
            print '|'+buf+'|'

    except socket.timeout:
        print 'time out'
    connection.close()
