# StreetFighter-AI-Bot

This project automates the gameplay of a Street Fighter character using an AI bot trained on gameplay data. The bot observes game states, predicts optimal actions, and simulates button inputs in real-time.

### 🎮 Emulator Integration (BizHawk)

This project is designed to work with the [BizHawk Emulator](http://tasvideos.org/BizHawk.html), which must be configured with a Lua script that does the following:

- Extracts current game state as JSON
- Sends the JSON data via a TCP socket to the Python bot
- Receives the bot's predicted button actions
- Applies those actions back into the emulator in real-time

⚠️ **Note**: The Lua script that connects BizHawk to the Python bot is **not included** in this repository. You must implement or configure it separately.

---

### 🔍 Description

- AI model predicts button inputs based on player positions, health, and movement states
- Uses a trained Keras model and Scikit-learn scaler
- Game state data is logged and used for model training (`GameData.xls`)
- Compatible with multiplayer simulation via `player1` or `player2` selection
  
## 📁 Project Structure

```bash

├── bot.py # Core AI logic to predict button actions
├── buttons.py # Button state management class
├── command.py # Button command packaging for both players
├── controller.py # Communication loop between bot and BizHawk emulator
├── game_state.py # Game state deserialization
├── model.py # Model training and evaluation script
├── player.py # Player state parsing
├── scaler.save # Scaler for input features
├── BotModel.h5 # Trained bot model
└── GameData.xls # Game data logs (created during run-time)

```
### 1. Train the Model (if needed)
```bash
python model.py
````

### 2. Start Bot Controller
``` bash

python controller.py 
```

### 3. Playing Notes
```bash
The controller script waits for game state updates and sends button commands in response.
Make sure the BizHawk emulator socket connection matches the specified port (9999 or 10000).
````
Requirements
```bash
Python 3.8 or above
TensorFlow
Scikit-learn
joblib
xlrd, xlwt, xlutils
````
Acknowledgements
This project is inspired by reinforcement and supervised learning in games, integrating emulator scripting and ML inference in real-time.
