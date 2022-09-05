# **Single obstacle avoidance agent learned using DQN.**
The environment built on custom 'Game' module.
The current implementation of Game module `Game-Cython BETA 0.1`
8/1/2022

## Prerequisite
```
pip install pygame==2.0.1
pip install numpy==1.19.5
```

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
