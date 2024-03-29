# -*- coding: utf-8 -*-
import socket, sys
import re
import random


#define msg
MSG_GAME_OVER='game-over \n'
# check | call | raise num | all_in | fold eol
MSG_CHECK='check \n'
MSG_CALL='call \n'
MSG_RAISE='raise 1 \n'
MSG_ALL_IN='all_in \n'
MSG_FOLD='fold \n'
MSG_CAN_SEND=[MSG_CHECK,MSG_CALL,MSG_RAISE,MSG_ALL_IN,MSG_FOLD]
#define msg end

#----------LOGIC PART-----------------
user_pid = []
user_jetton = []
user_money = []
user_order = [0,0,0,0,0,0,0,0,0,0]
match_number = 1
blind_number = 0
total_number = 0

def processSeatInfoMsg(seat_info_msg):
    #seat_info_msg
    #seat_info_msg = 'seat/ \nbutton: pid jetton money \nsmall blind: pid jetton money \nbig blind: pid jetton money \npid jetton money \n/seat \n'
    user_info = seat_info_msg.split('\n')

    user_pid_temp = user_info[1].split(' ')
    user_pid.append(user_pid_temp[1])
    user_jetton.append(user_pid_temp[2])
    user_money.append(user_pid_temp[3])

    user_pid_temp = user_info[2].split(' ')
    user_pid.append(user_pid_temp[2])
    user_jetton.append(user_pid_temp[3])
    user_money.append(user_pid_temp[4])

    user_number = 2

    if user_info[3] != '/seat ':
        user_pid_temp = user_info[3].split(' ')
        user_pid.append(user_pid_temp[2])
        user_jetton.append(user_pid_temp[3])
        user_money.append(user_pid_temp[4])

        i = 4

        while user_info[i] != '/seat ':
            user_pid_temp = user_info[i].split(' ')
            user_pid.append(user_pid_temp[0])
            user_jetton.append(user_pid_temp[1])
            user_money.append(user_pid_temp[2])
            user_number = i
            user_order[i] = user_number - 3
            i += 1

        user_order[0] =user_number - 2
        user_order[1] =user_number - 1
        user_order[2] =user_number

    else:

        user_order[0] = 1
        user_order[1] = 2

    print user_number


def processBlindMsg(blind_msg):
    #blind_msg
    # blind_msg = 'blind/ \npid: bet \n/blind \n'
    blind_info = blind_msg.split('\n')

    blind_number = blind_info[1].split(' ')[2]

    if blind_info[2] != '/blind ':
        if int(blind_number) < int(blind_info[1].split(' ')[2]):
            blind_number = blind_info[1].split(' ')[2]


def processHoldCardMsg(hold_cards_msg):
    #hold_cards_msg
    # hold_cards_msg = 'hold/ \ncolor point \ncolor point \n/hold \n'
    hold_cards_info = hold_cards_msg.split('\n')

    hold_card_color.append(hold_cards_info[1].split(' ')[0])

    if hold_cards_info[1].split(' ')[1] == 'J':
        hold_card_point.append('11')
    elif hold_cards_info[1].split(' ')[1] == 'Q':
        hold_card_point.append('12')
    elif hold_cards_info[1].split(' ')[1] == 'K':
        hold_card_point.append('13')
    elif hold_cards_info[1].split(' ')[1] == 'A':
        hold_card_point.append('14')
    else:
        hold_card_point.append(hold_cards_info[1].split(' ')[1])

    hold_card_color.append(hold_cards_info[2].split(' ')[0])
    if hold_cards_info[2].split(' ')[1] == 'J':
        hold_card_point.append('11')
    elif hold_cards_info[2].split(' ')[1] == 'Q':
        hold_card_point.append('12')
    elif hold_cards_info[2].split(' ')[1] == 'K':
        hold_card_point.append('13')
    elif hold_cards_info[2].split(' ')[1] == 'A':
        hold_card_point.append('14')
    else:
        hold_card_point.append(hold_cards_info[2].split(' ')[1])

    print hold_card_color
    print hold_card_point


def processInquireMsg(inquire_msg):
    #inquire_msg
    # inquire_msg = 'inquire/ \npid jetton money bet all_in \ntotal pot: num \n/inquire \n'
    inquire_info = inquire_msg.split('\n')

    user_number = len(inquire_info) - 1

    i = 2
    while inquire_info[i].split(' ')[0] != 'total':
        print 'Test'
        i += 1

    total_number = inquire_info[i].split(' ')[2]

    print total_number

    i = 0

    position = 0

    if user_number >= 4:
        while i < user_number:
            if user_pid[i] == pid:
                if i <= 2:
                    position = 1
                elif  user_number - i < 2:
                    position = 2

        if position == 1:
            if hold_card_point[0] == hold_card_point[1] and int(hold_card_point[0])>9:
                action_msg = 'raise ' + blind_number
            elif hold_card_color[0] == hold_card_color[1] and int(hold_card_point[0]) + int(hold_card_point[1]) > 24:
                action_msg = 'raise ' + blind_number
            elif hold_card_color[0] == hold_card_color[1] and max(int(hold_card_point[0]),int(hold_card_point[1])) == 12 and min(int(hold_card_point[0]),int(hold_card_point[1])) ==11:
                action_msg = 'raise ' + blind_number
            elif max(int(hold_card_point[0]),int(hold_card_point[1])) == 14 and min(int(hold_card_point[0]),int(hold_card_point[1])) ==13:
                action_msg = 'raise ' + blind_number
            elif hold_card_point[0] == hold_card_point[1] :
                action_msg = 'call '
            elif hold_card_color[0] == hold_card_color[1] and int(hold_card_point[0]) + int(hold_card_point[1]) > 17 and min(int(hold_card_point[0]),int(hold_card_point[1])) == 8:
                action_msg = 'call '
            else:
                action_msg = 'fold '


        elif position ==2:
            if hold_card_point[0] == hold_card_point[1]:
                action_msg = 'raise ' + blind_number
            elif hold_card_color[0] == hold_card_color[1] and max(int(hold_card_point[0]),int(hold_card_point[1])) >= 13:
                action_msg = 'raise ' + blind_number
            elif hold_card_color[0] == hold_card_color[1] and min(int(hold_card_point[0]),int(hold_card_point[1])) == 8:
                action_msg = 'raise ' + blind_number
            elif max(int(hold_card_point[0]),int(hold_card_point[1])) >= 13 and min(int(hold_card_point[0]),int(hold_card_point[1])) == 10:
                action_msg = 'raise ' + blind_number
            elif max(int(hold_card_point[0]),int(hold_card_point[1])) == 12 and min(int(hold_card_point[0]),int(hold_card_point[1])) ==11:
                action_msg = 'raise ' + blind_number
            elif max(int(hold_card_point[0]),int(hold_card_point[1])) == 11 and min(int(hold_card_point[0]),int(hold_card_point[1])) ==10:
                action_msg = 'raise ' + blind_number
            elif hold_card_color[0] == hold_card_color[1] and max(int(hold_card_point[0]),int(hold_card_point[1])) == 12 and min(int(hold_card_point[0]),int(hold_card_point[1])) >= 3:
                action_msg = 'call '
            elif hold_card_color[0] == hold_card_color[1] and max(int(hold_card_point[0]),int(hold_card_point[1])) == 11 and min(int(hold_card_point[0]),int(hold_card_point[1])) >= 7:
                action_msg = 'call '
            elif hold_card_color[0] == hold_card_color[1] and max(int(hold_card_point[0]),int(hold_card_point[1])) >= 8 and min(int(hold_card_point[0]),int(hold_card_point[1])) >= 6:
                action_msg = 'call '
            elif hold_card_color[0] == hold_card_color[1] and int(hold_card_point[0]) + int(hold_card_point[1]) >= 9 and min(int(hold_card_point[0]),int(hold_card_point[1])) >= 4:
                action_msg = 'call '
            else:
                action_msg = 'fold '


    else:
        if hold_card_point[0] == hold_card_point[1] and int(hold_card_point[0])>9:
            action_msg = 'raise ' + blind_number + ' '
        elif hold_card_color[0] == hold_card_color[1] and int(hold_card_point[0]) + int(hold_card_point[1]) > 24:
            action_msg = 'raise ' + blind_number + ' '
        elif hold_card_color[0] == hold_card_color[1] and max(int(hold_card_point[0]),int(hold_card_point[1])) == 12 and min(int(hold_card_point[0]),int(hold_card_point[1])) ==11:
            action_msg = 'raise ' + blind_number + ' '
        elif max(int(hold_card_point[0]),int(hold_card_point[1])) == 14 and min(int(hold_card_point[0]),int(hold_card_point[1])) ==13:
            action_msg = 'raise ' + blind_number + ' '
        elif hold_card_point[0] == hold_card_point[1] :
            action_msg = 'call '
        elif hold_card_color[0] == hold_card_color[1] and int(hold_card_point[0]) + int(hold_card_point[1]) > 17 and min(int(hold_card_point[0]),int(hold_card_point[1])) == 8:
            action_msg = 'call '
        else:
            action_msg = 'fold '


    action_msg += '\n'
    #TODO: ......................


def processFlopMsg(flop_mag):
    #flop_mag
    # flop_mag = 'flop/ \ncolor point \ncolor point \ncolor point \n/flop \n'
    flop_info = flop_mag.split('\n')

    i = 1
    while i <= 3:
        flop_card_color.append(flop_info[i].split(' ')[0])
        if flop_info[i].split(' ')[1] == 'J':
            flop_card_point.append('11')
        elif flop_info[i].split(' ')[1] == 'Q':
            flop_card_point.append('12')
        elif flop_info[i].split(' ')[1] == 'K':
            flop_card_point.append('13')
        elif flop_info[i].split(' ')[1] == 'A':
            flop_card_point.append('14')
        else:
            flop_card_point.append(flop_info[i].split(' ')[1])

        i += 1


def processTurnMsg(turn_msg):
    #turn_msg
    # turn_msg = 'turn/ \ncolor point \n/turn \n'
    turn_info = turn_msg.split('\n')

    flop_card_color.append(turn_info[1].split(' ')[0])
    if turn_info[1].split(' ')[1] == 'J':
        flop_card_point.append('11')
    elif turn_info[1].split(' ')[1] == 'Q':
        flop_card_point.append('12')
    elif turn_info[1].split(' ')[1] == 'K':
        flop_card_point.append('13')
    elif turn_info[1].split(' ')[1] == 'A':
        flop_card_point.append('14')
    else:
        flop_card_point.append(turn_info[1].split(' ')[1])


def processRiverMsg(river_msg):
    #river_msg
    # river_msg = 'river/ \ncolor point \n/river \n'
    river_info = river_msg.split('\n')

    flop_card_color.append(river_info[1].split(' ')[0])
    if river_info[1].split(' ')[1] == 'J':
        flop_card_point.append('11')
    elif river_info[1].split(' ')[1] == 'Q':
        flop_card_point.append('12')
    elif river_info[1].split(' ')[1] == 'K':
        flop_card_point.append('13')
    elif river_info[1].split(' ')[1] == 'A':
        flop_card_point.append('14')
    else:
        flop_card_point.append(river_info[1].split(' ')[1])

    print flop_card_color
    print flop_card_point


def processAllMsg(msg,client_socket):

    hold_card_color = []
    hold_card_point = []
    flop_card_color = []
    flop_card_point = []

    #identify msg ...
    msgReList = re.findall(r"(\w+?/\ \n.+?\n/\w+?\ \n)",msg,re.S)#解决粘包问题
    for msgReItem in msgReList:
        msg_arr = msgReItem.split('\n')
        if msg_arr[0] == 'seat/ ':
            # client_socket.send('seat/ ')
            n=0
        elif msg_arr[0] == 'blind/ ':
            # client_socket.send('blind/ ')
            n=0
        elif msg_arr[0] == 'hold/ ':
            # client_socket.send('hold/ ')
            n=0
        elif msg_arr[0] == 'inquire/ ':
            # client_socket.send('fold \n')
            ranInt = random.randint(0,len(MSG_CAN_SEND)-1)
            client_socket.send(MSG_CAN_SEND[ranInt])
            n=0
        elif msg_arr[0] == 'flop/ ':
            # client_socket.send('flop/ ')
            n=0
        elif msg_arr[0] == 'turn/ ':
            # client_socket.send('turn/ ')
            n=0
        elif msg_arr[0] == 'river/ ':
            # client_socket.send('river/ ')
            n=0



#----------LOGIC PART-----------------



if len(sys.argv) != 6:
    print 'Parameter not mate, notice must use like this:'
    print '\rpython client.py [ip] [port]'
    sys.exit(0)

#获得的相关信息
server_ip = sys.argv[1]
server_port = int(sys.argv[2])
client_ip = sys.argv[3]
client_port = int(sys.argv[4])
pid = sys.argv[5]

#链接程序
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = (server_ip, server_port)
client_addr = (client_ip, client_port)

#bind client_addr
client_socket.bind(client_addr)

#connect server_addr
client_socket.connect(server_addr)

# client_socket.settimeout(2000)

#register on server...
client_socket.send('reg: '+pid+' Neo \n')

buf_len=4096
# buf = ''
# has_in = False
while 1:
    data = client_socket.recv(buf_len)
    print 'data: ['+data+']'
    if data== MSG_GAME_OVER:
        break
    else:
        processAllMsg(data,client_socket)

    # if len(data) == buf_len: #It mey casue a bug, if the msg len is exactly buf_len, it will wait for the next msg to recv..Ugly!
    #     if has_in==False:
    #         buf =''
    #         has_in=True
    #     buf += data
    # else:
    #     if has_in==True:
    #         buf += data
    #         has_in = False
    #     else:
    #         buf = data
    #
    # print 'data: ['+data+']'
    # if has_in==False:
    #     print 'buf: ['+buf+']'

client_socket.close()
sys.exit(0)
