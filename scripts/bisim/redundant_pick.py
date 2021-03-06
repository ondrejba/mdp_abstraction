import envs.redundant_pick as redundant_pick
from algorithms import bisimulation

partition = bisimulation.partition_iteration(redundant_pick)

print("state partition:")
for block in partition:
    print("block:", list(block))