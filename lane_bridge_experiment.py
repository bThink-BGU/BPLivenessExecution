import gym
import os
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN
from stable_baselines.bench import Monitor
from lane_bridge import *

def evaluate_model(model):
    total_rewards = 0
    for i in range(1000):
        observation = env.reset()
        reward_sum = 0
        counter = 0
        while True:
            # env.render()
            action, _states = model.predict(observation)
            observation, reward, done, info = env.step(action)
            reward_sum += reward
            counter += 1
            #print(action, observation, reward, done, info)
            if done:
                break
        total_rewards += reward_sum
    print(1+(total_rewards/1000))

experiments = [
    {
        "name": "dqn1",
        "n": 1,
        "double_q": False,
        "prioritized_replay": False,
        "total_timesteps": 100000,
        "layers": 5
    },
    {
        "name": "dqn2",
        "n": 2,
        "double_q": False,
        "prioritized_replay": False,
        "total_timesteps": 250000,
        "layers": 6
    },
    {
        "name": "dqn3",
        "n": 3,
        "double_q": False,
        "prioritized_replay": False,
        "total_timesteps": 400000,
        "layers": 7
    },
    {
        "name": "dqn4",
        "n": 4,
        "double_q": False,
        "prioritized_replay": False,
        "total_timesteps": 550000,
        "layers": 8
    },
    {
        "name": "ddqn1",
        "n": 1,
        "double_q": True,
        "prioritized_replay": False,
        "total_timesteps": 100000,
        "layers": 5
    },
    {
        "name": "ddqn2",
        "n": 2,
        "double_q": True,
        "prioritized_replay": False,
        "total_timesteps": 250000,
        "layers": 6
    },
    {
        "name": "ddqn3",
        "n": 3,
        "double_q": True,
        "prioritized_replay": False,
        "total_timesteps": 400000,
        "layers": 7
    },
    {
        "name": "ddqn4",
        "n": 4,
        "double_q": True,
        "prioritized_replay": False,
        "total_timesteps": 550000,
        "layers": 8
    },
    {
        "name": "per1",
        "n": 1,
        "double_q": False,
        "prioritized_replay": True,
        "total_timesteps": 100000,
        "layers": 5
    },
    {
        "name": "per2",
        "n": 2,
        "double_q": False,
        "prioritized_replay": True,
        "total_timesteps": 250000,
        "layers": 6
    },
    {
        "name": "per3",
        "n": 3,
        "double_q": False,
        "prioritized_replay": True,
        "total_timesteps": 400000,
        "layers": 7
    },
    {
        "name": "per4",
        "n": 4,
        "double_q": False,
        "prioritized_replay": True,
        "total_timesteps": 550000,
        "layers": 8
    },
]

for e in experiments:
    print(e)
    # Create log dir
    log_dir = "/tmp/"+ e["name"] +"/"
    os.makedirs(log_dir, exist_ok=True)
    b_program_settings["n_blue_cars"] = e["n"]
    env = gym_env_generator(episode_timeout=50)
    #env = gym.make('CartPole-v1')
    env = Monitor(env, log_dir)
    policy_kwargs = dict(layers=[e["layers"]])
    model = DQN("MlpPolicy", 
                env, 
                verbose=1, 
                exploration_fraction=0.9,
                exploration_final_eps=0,
                learning_rate=0.001,
                learning_starts=100,
                policy_kwargs = policy_kwargs,
                double_q = e["double_q"],
                prioritized_replay = e["prioritized_replay"])
    model.learn(total_timesteps=e["total_timesteps"])
    model.save(e["name"])
    del model # remove to demonstrate saving and loading
    model = DQN.load(e["name"])
    evaluate_model(model)
    env.close()