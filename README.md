# **Single obstacle avoidance agent learned using DQN.**

# Prerequisite
    pip install pygame==2.0.1
    pip install numpy==1.19.5

    'Install working tensorflow gpu version on your system'
    pip install tensorflow-gpu

# Creating custom environment
    ----
    python create_env.py
    ----

    Key binding
    ----
    c -> Create new shape
    s -> Locate current shape
    d -> Delete last located shape
    q -> Decrease vertex count of current shape
    e -> Increase vertex count of current shape
    ↑ -> Scale up current shape
    ↓ -> Scale down current shape
    ← -> Rotate left
    → -> Rotate right
    0 -> Create static shape
    1 -> Create dynamic shape
    f -> Save current environment and exit

# Training
    In train.py
    Set optional HYPERPARAMETERs
    Set CURRENT_TRAIN_ID to unique value to log train info

    ----
    python train.py
    ----

# Test
    ----
    python play.py
    ----

    Navigate to trained model in log folder.
