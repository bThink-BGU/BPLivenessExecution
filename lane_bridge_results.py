import matplotlib.pyplot as plt
from numpy.core.fromnumeric import mean
import numpy as np
import os
FOLDER_NAME = "/Users/tomyaacov/Downloads/16_2_10_8"

experiments = {
    "1_CAR": {"DQN": "dqn1", "DDQN": "ddqn1", "PER": "per1"},
    "2_CAR": {"DQN": "dqn2", "DDQN": "ddqn2", "PER": "per2"},
    "3_CAR": {"DQN": "dqn3", "DDQN": "ddqn3", "PER": "per3"}
}

def get_rewards(file):
    rewards = []
    steps = []
    with open(file) as f:
        for l in f.readlines()[2:]:
            rewards.append(float(l.split(",")[0]))
            steps.append(int(l.split(",")[1]))
    steps = list(np.cumsum(steps))
    final_r = []
    final_s = []
    for i in range(1000, len(rewards), 1):
        final_r.append(mean(rewards[i-1000:i]))
        final_s.append(steps[i])
    return final_r, final_s

for k1,v1 in experiments.items():
    for k2,v2 in v1.items():
        r, s = get_rewards(os.path.join(FOLDER_NAME, v2, "monitor.csv"))
        s = [x/1000 for x in s]
        plt.plot(s, r, label=k2)
    plt.ylabel('last 1e3 mean reward')
    plt.xlabel('events (1e3)')
    plt.legend()
    plt.savefig(k1 + ".pdf")
    plt.close()