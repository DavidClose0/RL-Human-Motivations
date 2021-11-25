from os.path import exists
from red_gym_env import RedGymEnv
import gym
from stable_baselines3 import A2C, PPO
from stable_baselines3.common import env_checker

env_config = {
                'headless': True, 
                'action_freq': 5, 'init_state': '../init.state', 'max_steps': 150, 
                'gb_path': '../PokemonRed.gb', 'debug': False
            }

env = RedGymEnv(env_config)

env_checker.check_env(env)

# env = gym.make('CartPole-v1')
learn_steps = 40
file_name = 'poke_'
if exists(file_name+'.zip'):
    print('loading checkpoint')
    model = PPO.load(file_name, env=env)
else:
    model = PPO('CnnPolicy', env, verbose=1, n_steps=2048*6, batch_size=128, n_epochs=3, gamma=0.99)

for i in range(learn_steps):
    model.learn(total_timesteps=80000)
    model.save(file_name+str(i))
