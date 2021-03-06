STATES = [1, 2, 3, 4, 5]
INITIAL_STATES = [1, 2, 3, 4]
GOAL_STATE = 5
ACTIONS = [1, 2, 3, 4]

P = {}
R = {}

for state in STATES:

    if state == GOAL_STATE:
        R[state] = 1
    else:
        R[state] = 0

    for action in ACTIONS:
        if state == action:
            P[(state, action)] = GOAL_STATE
        else:
            P[(state, action)] = state

assert len(P.keys()) == (4 * len(STATES))
assert len(R.keys()) == len(STATES)