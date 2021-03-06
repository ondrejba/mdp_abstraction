import argparse
import os
import copy as cp
import numpy as np
from envs.continuous_3 import ContinuousEnv3
from algorithms import online_homomorphism_g
import evaluation
import model_utils
import vis_utils

os.environ["CUDA_VISIBLE_DEVICES"] = ""


def gather_experience(env, num):

    transitions = []

    for _ in range(num // 5):

        env.reset()

        for _ in range(5):

            state = cp.deepcopy(env.state)
            action = np.random.uniform(0, 2)
            reward, next_state, done = env.step(action)

            transitions.append((state, action, reward, next_state, done))

            if done:
                break

    return transitions


def sample_actions(state):

    num = 10
    start = 0
    end = 2
    actions = list(np.linspace(start, end, num=num))
    return actions


def main(args):

    env = ContinuousEnv3()
    g = model_utils.BalancedMLP([1], [8, 16], 0.001, 32, 0.0, verbose=True)

    def visualize_b(state_action_partition):

        vis_utils.plot_background(env, show=False)
        vis_utils.plot_decision_boundary(g, env.STATE_ACTION_MAP.shape[1], env.STATE_ACTION_MAP.shape[0], show=False)
        vis_utils.plot_state_action_partition(state_action_partition, show=True)

    def visualize_sb(state_partition):

        vis_utils.plot_background(env, show=False)
        vis_utils.plot_state_partition(state_partition, show=True)

    experience = gather_experience(env, args.num_experience)
    homo = online_homomorphism_g.OnlineHomomorphismG(experience, g, sample_actions, args.state_action_slit_threshold,
                                                     args.state_split_threshold, 20, visualize_b=visualize_b,
                                                     visualize_sb=visualize_sb)
    homo.partition_iteration()

    hits, total = evaluation.overlap(env, list(homo.partition))
    print("{:.2f}% accuracy ({:d}/{:d})".format((hits / total) * 100, hits, total))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-e", "--num-experience", type=int, default=2000)
    parser.add_argument("-a", "--state-action-split-threshold", type=int, default=200)
    parser.add_argument("-s", "--state-split-threshold", type=int, default=200)

    parsed = parser.parse_args()
    main(parsed)
