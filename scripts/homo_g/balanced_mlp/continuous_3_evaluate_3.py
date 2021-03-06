import argparse
import os
import copy as cp
import numpy as np
from envs.continuous_3 import ContinuousEnv3
from algorithms import online_homomorphism_g
import evaluation, model_utils, log_utils


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


def run(num_experience, state_action_threshold, state_threshold):

    env = ContinuousEnv3()
    g = model_utils.BalancedMLP([1], [8, 16], 0.001, 32, 0.0, verbose=True)

    experience = gather_experience(env, num_experience)
    homo = online_homomorphism_g.OnlineHomomorphismG(experience, g, sample_actions, state_action_threshold,
                                                     state_threshold, 20)
    homo.partition_iteration()

    hits, total = evaluation.overlap(env, list(homo.partition))
    accuracy = hits / total

    return accuracy


def main(args):

    os.environ["CUDA_VISIBLE_DEVICES"] = ""

    NUM_RUNS = 50
    NUM_EXPERIENCE = 2000
    SPLIT_THRESHOLD_LIST = [50, 100, 200, 500]
    SAVE_DIR = "results/homo_g/balanced_mlp"
    SAVE_FILE = "continuous_3_evaluation_3.pickle"
    SAVE_PATH = os.path.join(SAVE_DIR, SAVE_FILE)

    # maybe create dir
    if not os.path.isdir(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # load results if already exist
    if os.path.isfile(SAVE_PATH):
        results = log_utils.read_pickle(SAVE_PATH)
    else:
        results = {}

    for t1 in SPLIT_THRESHOLD_LIST:

        for t2 in SPLIT_THRESHOLD_LIST:

            for run_idx in range(NUM_RUNS):

                key = (t1, t2, run_idx)

                # skip if this setting is already in results
                if key in results:
                    continue

                accuracy = run(NUM_EXPERIENCE, t1, t2)
                results[key] = accuracy

                # save results after each run
                log_utils.write_pickle(SAVE_PATH, results)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parsed = parser.parse_args()
    main(parsed)
