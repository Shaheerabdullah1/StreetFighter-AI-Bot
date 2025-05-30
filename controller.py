import socket
import json

from xlwt import Workbook
import xlrd
from xlutils.copy import copy

from os.path import exists
from game_state import GameState
#from bot import fight
import sys
from bot import Bot
import xlwt


def connect(port):
    #For making a connection with the game
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    (client_socket, _) = server_socket.accept()
    print ("Connected to game!")
    return client_socket

def send(client_socket, command):
    #This function will send your updated command to Bizhawk so that game reacts according to your command.
    command_dict = command.object_to_dict()
    pay_load = json.dumps(command_dict).encode()
    client_socket.sendall(pay_load)

def receive(client_socket):
    #receive the game state and return game state
    pay_load = client_socket.recv(4096)
    input_dict = json.loads(pay_load.decode())
    game_state = GameState(input_dict)
    return game_state


def main():
    if sys.argv[1] == '1':
        client_socket = connect(9999)
    elif sys.argv[1] == '2':
        client_socket = connect(10000)
    current_game_state = None
    bot = Bot()

    wb = None
    sheet1 = None
    if exists('GameData.xls'):
        rb = xlrd.open_workbook('GameData.xls', formatting_info=True)
        r_sheet = rb.sheet_by_index(0)
        rn = r_sheet.nrows
        wb = copy(rb)
        sheet1 = wb.get_sheet(0)

    else:

        wb = Workbook()
        sheet1 = wb.add_sheet('GameData')
        rn = 0
        sheet1.write(rn, 1, 'Timer')
        sheet1.write(rn, 2, 'fight result')
        sheet1.write(rn, 3, 'has_round_started')
        sheet1.write(rn, 4, 'is_round_over')

        sheet1.write(rn, 5, 'player1_id')
        sheet1.write(rn, 6, 'player1_health')
        sheet1.write(rn, 7, 'player1_x_coord')
        sheet1.write(rn, 8, 'player1_y_coord')
        sheet1.write(rn, 9, 'player1_is_jumping')
        sheet1.write(rn, 10, 'player1_is_crouching')
        sheet1.write(rn, 11, 'player1_is_player_in_move')
        sheet1.write(rn, 12, 'player1_move_id')

        sheet1.write(rn, 13, 'player1_button_up')
        sheet1.write(rn, 14, 'player1_button_down')
        sheet1.write(rn, 15, 'player1_button_right')
        sheet1.write(rn, 16, 'player1_button_left')
        sheet1.write(rn, 17, 'player1_button_select')
        sheet1.write(rn, 18, 'player1_button_start')
        sheet1.write(rn, 19, 'player1_button_Y')
        sheet1.write(rn, 20, 'player1_button_B')
        sheet1.write(rn, 21, 'player1_button_X')
        sheet1.write(rn, 22, 'player1_button_A')
        sheet1.write(rn, 23, 'player1_button_L')
        sheet1.write(rn, 24, 'player1_button_R')

        sheet1.write(rn, 25, 'player2_id')
        sheet1.write(rn, 26, 'player2_health')
        sheet1.write(rn, 27, 'player2_x_coord')
        sheet1.write(rn, 28, 'player2_y_coord')
        sheet1.write(rn, 29, 'player2_is_jumping')
        sheet1.write(rn, 30, 'player2_is_crouching')
        sheet1.write(rn, 31, 'player2_is_player_in_move')
        sheet1.write(rn, 32, 'player2_move_id')

        sheet1.write(rn, 33, 'player2_button_up')
        sheet1.write(rn, 34, 'player2_button_down')
        sheet1.write(rn, 35, 'player2_button_right')
        sheet1.write(rn, 36, 'player2_button_left')
        sheet1.write(rn, 37, 'player2_button_select')
        sheet1.write(rn, 38, 'player2_button_start')
        sheet1.write(rn, 39, 'player2_button_Y')
        sheet1.write(rn, 40, 'player2_button_B')
        sheet1.write(rn, 41, 'player2_button_X')
        sheet1.write(rn, 42, 'player2_button_A')
        sheet1.write(rn, 43, 'player2_button_L')
        sheet1.write(rn, 44, 'player2_button_R')
        rn += 1
    while (current_game_state is None) or (not current_game_state.is_round_over):

        current_game_state = receive(client_socket)
        bot_command = bot.fight(current_game_state, sys.argv[1])
        send(client_socket, bot_command)

        if current_game_state is not None:

            if current_game_state.player2.player_buttons.up:
                print('Up')
            if current_game_state.player2.player_buttons.down:
                print('Down')
            if current_game_state.player2.player_buttons.left:
                print('Left')
            if current_game_state.player2.player_buttons.right:
                print('Right')

            if current_game_state.player2.player_buttons.L:
                print('L')
            if current_game_state.player2.player_buttons.R:
                print('R')
            if current_game_state.player2.player_buttons.A:
                print('A')
            if current_game_state.player2.player_buttons.B:
                print('B')

            if current_game_state.player2.player_buttons.X:
                print('X')
            if current_game_state.player2.player_buttons.Y:
                print('Y')

            sheet1.write(rn,1,current_game_state.timer)
            sheet1.write(rn,2,current_game_state.fight_result)
            sheet1.write(rn,3,current_game_state.has_round_started)
            sheet1.write(rn,4,current_game_state.is_round_over)

            sheet1.write(rn,5,current_game_state.player1.player_id)
            sheet1.write(rn,6,current_game_state.player1.health)
            sheet1.write(rn,7,current_game_state.player1.x_coord)
            sheet1.write(rn,8,current_game_state.player1.y_coord)
            sheet1.write(rn,9,current_game_state.player1.is_jumping)
            sheet1.write(rn,10,current_game_state.player1.is_crouching)
            sheet1.write(rn,11,current_game_state.player1.is_player_in_move)
            sheet1.write(rn,12,current_game_state.player1.move_id)

            sheet1.write(rn,13,current_game_state.player1.player_buttons.up)
            sheet1.write(rn,14,current_game_state.player1.player_buttons.down)
            sheet1.write(rn,15,current_game_state.player1.player_buttons.right)
            sheet1.write(rn,16,current_game_state.player1.player_buttons.left)
            sheet1.write(rn,17,current_game_state.player1.player_buttons.select)
            sheet1.write(rn,18,current_game_state.player1.player_buttons.start)
            sheet1.write(rn,19,current_game_state.player1.player_buttons.Y)
            sheet1.write(rn,20,current_game_state.player1.player_buttons.B)
            sheet1.write(rn,21,current_game_state.player1.player_buttons.X)
            sheet1.write(rn,22,current_game_state.player1.player_buttons.A)
            sheet1.write(rn,23,current_game_state.player1.player_buttons.L)
            sheet1.write(rn,24,current_game_state.player1.player_buttons.R)

            sheet1.write(rn,25,current_game_state.player2.player_id)
            sheet1.write(rn,26,current_game_state.player2.health)
            sheet1.write(rn,27,current_game_state.player2.x_coord)
            sheet1.write(rn,28,current_game_state.player2.y_coord)
            sheet1.write(rn,29,current_game_state.player2.is_jumping)
            sheet1.write(rn,30,current_game_state.player2.is_crouching)
            sheet1.write(rn,31,current_game_state.player2.is_player_in_move)
            sheet1.write(rn,32,current_game_state.player2.move_id)

            sheet1.write(rn,33,current_game_state.player2.player_buttons.up)
            sheet1.write(rn,34,current_game_state.player2.player_buttons.down)
            sheet1.write(rn,35,current_game_state.player2.player_buttons.right)
            sheet1.write(rn,36,current_game_state.player2.player_buttons.left)
            sheet1.write(rn,37,current_game_state.player2.player_buttons.select)
            sheet1.write(rn,38,current_game_state.player2.player_buttons.start)
            sheet1.write(rn,39,current_game_state.player2.player_buttons.Y)
            sheet1.write(rn,40,current_game_state.player2.player_buttons.B)
            sheet1.write(rn,41,current_game_state.player2.player_buttons.X)
            sheet1.write(rn,42,current_game_state.player2.player_buttons.A)
            sheet1.write(rn,43,current_game_state.player2.player_buttons.L)
            sheet1.write(rn,44,current_game_state.player2.player_buttons.R)
            rn += 1

    wb.save('GameData.xls')


if __name__ == '__main__':
    main()
