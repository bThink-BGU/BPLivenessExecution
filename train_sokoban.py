import os
import sys
import matplotlib.pyplot as plt
from bp_env import BPEnv
from sokoban import *
from q_learning import *
from sokoban_maps import maps
import sys

map_key = int(sys.argv[1])
map_value = maps[map_key]

env = BPEnv()
env.set_bprogram_generator(init_bprogram)

pygame_settings["display"] = False
map_settings["map"] = map_value

Q, results, episodes, mean_reward = qlearning(environment=env,
                                              num_episodes=10000,
                                              episode_timeout=100,
                                              alpha=0.1,
                                              gamma=0.99,
                                              testing=True,
                                              seed=1,
                                              glie=glie_10)

plt.plot(episodes, mean_reward)
plt.ylabel('mean reward')
plt.xlabel('episode')
plt.title(os.path.basename(sys.argv[0])[:-3] + "_" + sys.argv[1] )
plt.savefig(os.path.basename(sys.argv[0])[:-3] + "_" + sys.argv[1] + ".pdf")
event_runs = []
rewards_sum = 0
for i in range(100):
    reward, event_run = run(env, Q, i, 100, True)
    if event_run not in event_runs:
        event_runs.append(event_run)
    rewards_sum += reward
    
print(map_key, rewards_sum / 100)
# print(event_runs)
# print(rewards_sum)
import pickle
pickle_out = open("models/Q_f_"+str(map_key)+".pickle", "wb")
pickle.dump(Q, pickle_out)
pickle_out.close()