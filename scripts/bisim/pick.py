import envs.pick as pick
from algorithms import bisimulation

partition = bisimulation.partition_iteration(pick)

print("state partition:")
for block in partition:
    print("block:", list(block))