from env import Environment
from model import DQN
from tkinter import Tk, filedialog

Tk().withdraw()

# Model path
path = filedialog.askopenfilename()

# Load model
model = DQN(path)
# Test model
model.epsilon = 0

# Prepare env
env = Environment('test_env.json')


# Mainloop
while env.running:
    state = env.reset()
    while not env.over:
        action = model.predict_action(state)
        reward, state = env.step(action)
