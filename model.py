import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load the game data
gamedata = pd.read_csv("GameData.csv")

# Drop unnecessary columns
gamedata = gamedata.drop(['has_round_started', 'is_round_over', 'player1_is_jumping', 'player1_is_crouching',
                          'player2_health', 'player1_id', 'player1_move_id', 'player2_move_id', 'player2_id',
                          'player1_is_player_in_move', 'player2_is_player_in_move', 'fight result',
                          'player1_button_start', 'player1_button_select', 'player2_button_start',
                          'player2_button_select', 'player1_button_right', 'player1_button_left',
                          'player1_button_up', 'player1_button_down', 'player1_button_L', 'player1_button_R',
                          'player1_button_X', 'player1_button_Y', 'player1_button_A', 'player1_button_B'],
                         axis=1)

# Calculate the difference in x and y coordinates
gamedata['x_diff'] = abs(gamedata['player1_x_coord'] - gamedata['player2_x_coord'])
gamedata['y_diff'] = abs(gamedata['player1_y_coord'] - gamedata['player2_y_coord'])

# Prepare the input features (X) and target labels (y)
X = gamedata.drop(['player2_button_up', 'player2_button_down', 'player2_button_left', 'player2_button_right',
                   'player2_button_L', 'player2_button_R', 'player2_button_A', 'player2_button_X',
                   'player2_button_B', 'player2_button_Y'], axis=1)
y = gamedata[['player2_button_up', 'player2_button_down', 'player2_button_left', 'player2_button_right',
              'player2_button_L', 'player2_button_R', 'player2_button_A', 'player2_button_X',
              'player2_button_B', 'player2_button_Y']]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale numerical features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define the model architecture
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(y_train.shape[1], activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=1)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print('Test Loss:', loss)
print('Test Accuracy:', accuracy)

# Make predictions
predictions = model.predict(X_test)
predicted_buttons = (predictions > 0.1)

# Convert boolean values to True/False
predicted_buttons = predicted_buttons.astype(bool)

# Print the predicted boolean values
for i in predicted_buttons:
    print(i)

# Save the model
model.save('BotModel.h5')

# Save the scaler
scaler_filename = 'scaler.save'
import joblib
joblib.dump(scaler, scaler_filename)


# Load the scaler
scaler = joblib.load('scaler.save')

# Load the model
model = tf.keras.models.load_model('BotModel.h5')

# Load new game data for prediction
new_gamedata = pd.read_csv("NewGameData.csv")

# Drop unnecessary columns
new_gamedata = new_gamedata.drop(['has_round_started', 'is_round_over', 'player1_is_jumping', 'player1_is_crouching',
                                  'player2_health', 'player1_id', 'player1_move_id', 'player2_move_id', 'player2_id',
                                  'player1_is_player_in_move', 'player2_is_player_in_move', 'fight result',
                                  'player1_button_start', 'player1_button_select', 'player2_button_start',
                                  'player2_button_select', 'player1_button_right', 'player1_button_left',
                                  'player1_button_up', 'player1_button_down', 'player1_button_L', 'player1_button_R',
                                  'player1_button_X', 'player1_button_Y', 'player1_button_A', 'player1_button_B'],
                                 axis=1)

# Calculate the difference in x and y coordinates
new_gamedata['x_diff'] = abs(new_gamedata['player1_x_coord'] - new_gamedata['player2_x_coord'])
new_gamedata['y_diff'] = abs(new_gamedata['player1_y_coord'] - new_gamedata['player2_y_coord'])

# Scale the new game data using the loaded scaler
new_gamedata_scaled = scaler.transform(new_gamedata)



