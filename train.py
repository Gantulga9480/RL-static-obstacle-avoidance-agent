from env import Environment
from model import DQN, ReplayBuffer

MAX_REPLAY_BUFFER = 1500
TARGET_NET_UPDATE_FREQ = 18
MAIN_NET_TRAIN_FREQ = 3
EPISODE_STEP = 5000
CURRENT_TRAIN_ID = 'model_id'

model = DQN()
env = Environment('train_env.json')
replay_buffer = ReplayBuffer(MAX_REPLAY_BUFFER, model.BATCH_SIZE)

r_sum = 0
step_count = 0
episode_count = 0
last_avg_reward = 0

while env.running:
    state = env.reset()
    while not env.over:
        action = model.predict_action(state)
        reward, n_state = env.step(action)

        step_count += 1
        r_sum += reward

        if step_count > EPISODE_STEP:
            env.over = True
            episode_count += 1
            step_count = 1
            avg_reward = round(r_sum/EPISODE_STEP, 2)
            r_sum = 0
            if avg_reward > last_avg_reward:
                last_avg_reward = avg_reward
                path = '/'.join([
                    'model',
                    CURRENT_TRAIN_ID,
                    f'model_{episode_count}_{avg_reward}'
                ])
                model.save(path)

        replay_buffer.push([state, action, n_state, reward, env.over])
        state = n_state

        if replay_buffer.trainable:
            if step_count % MAIN_NET_TRAIN_FREQ == 0:
                model.train(replay_buffer.sample(model.BATCH_SIZE, 0.6))
            model.decay_epsilon()
            if model.epsilon == model.MIN_EPSILON:
                model.epsilon = 0.2
            if step_count % TARGET_NET_UPDATE_FREQ == 0:
                model.update_target()

        info = ' '.join([
            f'ep: {episode_count}',
            f'e: {model.epsilon}',
            f'r: {reward}'
        ])
        print(info)

path = '/'.join(['model', CURRENT_TRAIN_ID, 'model'])
model.save(path)
