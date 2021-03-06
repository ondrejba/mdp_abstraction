import os
import numpy as np
import log_utils
import seaborn as sns
import matplotlib.pyplot as plt

LOAD_DIR_1 = "results/homo_g_dict/balanced_mlp"
LOAD_FILE_1 = "experiment_1_thresholds.pickle"
LOAD_PATH_1 = os.path.join(LOAD_DIR_1, LOAD_FILE_1)

LOAD_DIR_2 = "results/homo_g/balanced_mlp"
LOAD_FILE_2 = "experiment_1_thresholds.pickle"
LOAD_PATH_2 = os.path.join(LOAD_DIR_2, LOAD_FILE_2)

NUM_RUNS = 50
NUM_EXPERIENCE_LIST = [200, 500, 1000]
SPLIT_THRESHOLD_LIST = [50, 100, 200]

results_1 = log_utils.read_pickle(LOAD_PATH_1)
results_2 = log_utils.read_pickle(LOAD_PATH_2)

results_array = np.zeros((len(NUM_EXPERIENCE_LIST), len(SPLIT_THRESHOLD_LIST)))

for i, num_experience in enumerate(NUM_EXPERIENCE_LIST):

    for j, split_threshold in enumerate(SPLIT_THRESHOLD_LIST):

        accuracies = []

        for run_idx in range(NUM_RUNS):

            key = (num_experience, split_threshold, run_idx)

            if key in results_1 and key in results_2:

                accuracies.append(((results_1[key] / results_2[key]) - 1) * 100)

        if len(accuracies) > 0:
            mean_accuracy = np.mean(accuracies)
            print(num_experience, split_threshold, mean_accuracy)
            results_array[i, j] = mean_accuracy

sns.heatmap(results_array, xticklabels=SPLIT_THRESHOLD_LIST, yticklabels=NUM_EXPERIENCE_LIST, annot=True, cbar=False)
plt.xlabel("split threshold for state-action blocks")
plt.ylabel("num experience")
plt.show()
