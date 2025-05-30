from command import Command
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from buttons import Buttons
import joblib


class Bot:

    def __init__(self):
        self.fire_code = ["<", "!<", "v+<", "!v+!<", "v", "!v", "v+>", "!v+!>", ">+Y", "!>+!Y"]
        self.exe_code = 0
        self.start_fire = True
        self.remaining_code = []
        self.my_command = Command()
        self.buttn = Buttons()
        self.bot_model = tf.keras.models.load_model('BotModel.h5')
        self.scaler = joblib.load('scaler.save')


    def setButtonsFalse(self):

        self.buttn.up = False
        self.buttn.down = False
        self.buttn.left = False
        self.buttn.right = False
        self.buttn.L = False
        self.buttn.R = False
        self.buttn.A = False
        self.buttn.B = False
        self.buttn.X = False
        self.buttn.Y = False

    def fight(self, current_game_state, player):

        if player == "1":

            single_input = np.array([[current_game_state.timer, current_game_state.player2.health, current_game_state.player2.x_coord, current_game_state.player2.y_coord, current_game_state.player1.x_coord,	current_game_state.player1.y_coord,	current_game_state.player1.is_jumping,	current_game_state.player1.is_crouching, abs(current_game_state.player1.x_coord-current_game_state.player1.x_coord), abs(current_game_state.player1.y_coord-current_game_state.player1.y_coord)]])

            scaled_input = self.scaler.transform(single_input)

            predictions = self.bot_model.predict(scaled_input)
            predicted_buttons = (predictions > 0.1)
            predicted_buttons = predicted_buttons.astype(bool)

            self.setButtonsFalse()
            if predicted_buttons[0][0]:
                self.buttn.up = True

            if predicted_buttons[0][1]:
                self.buttn.down = True

            if predicted_buttons[0][2]:
                self.buttn.left = True

            if predicted_buttons[0][3]:
                self.buttn.right = True

            if predicted_buttons[0][4]:
                self.buttn.L = True

            if predicted_buttons[0][5]:
                self.buttn.R = True

            if predicted_buttons[0][6]:
                self.buttn.A = True

            if predicted_buttons[0][7]:
                self.buttn.X = True

            if predicted_buttons[0][8]:
                self.buttn.B = True

            if predicted_buttons[0][9]:
                self.buttn.Y = True

            self.my_command.player_buttons = self.buttn

        elif player == "2":
            self.my_command.player2_buttons = self.buttn

        return self.my_command
