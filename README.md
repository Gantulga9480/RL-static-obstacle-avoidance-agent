# **Single obstacle avoidance agent learned using DQN.**
The environment built on custom 'Game' module.
The current implementation of Game module `Game-Cython BETA 0.1`
8/1/2022

## Prerequisite
Install working tensorflow gpu version on your system
```
pip install tensorflow-gpu
```

## Building Game module
In order to run this environment the user need to build for your python version.

```
python cython_setup.py build_ext --inplace
```

## Creating custom environment
```
python create_env.py
```

## Key binding

<ul>
    <li>c -> Create new shape</li>
    <li>s -> Locate current shape</li>
    <li>d -> Delete last located shape</li>
    <li>q -> Decrease vertex count of current shape</li>
    <li>e -> Increase vertex count of current shape</li>
    <li>↑ -> Scale up current shape</li>
    <li>↓ -> Scale down current shape</li>
    <li>← -> Rotate left</li>
    <li>→ -> Rotate right</li>
    <li>0 -> Create static shape</li>
    <li>1 -> Create dynamic shape</li>
    <li>f -> Save current environment and exit</li>
</ul>

### Note on creating new environment
Only ONE dynamic object has to be created.
The model trained on only one dynamic agent.
So the trained model has some initial knowledge about
the shape and size of the object acting upon.
Keep the file structure be like test environment file.
The dynamic object has type of 1 and placed at the bottom of environment file.
We encourage you to use the pre-defined test env environment file.
You may change the initial position for your environment. So the agent
wont stuck insided of other static shapes.

## Training
In train.py
Set optional HYPERPARAMETERs
Set CURRENT_TRAIN_ID to unique value to log train info
```
python train.py
```

## Testing
```
python play.py
```
Navigate to trained model in log folder.
