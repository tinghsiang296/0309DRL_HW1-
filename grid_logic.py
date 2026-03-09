import random

def policy_evaluation(n, end_pos, obstacles, policy, gamma=0.9, theta=0.001):
    """
    Perform Iterative Policy Evaluation for a fixed policy.
    Returns: V dict where V is a dict of values.
    """
    V = {(r, c): 0.0 for r in range(n) for c in range(n)}
    end_r, end_c = map(int, end_pos.split(','))
    obs_list = [tuple(map(int, o.split(','))) for o in obstacles]
    
    actions = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1)
    }

    iter_count = 0
    while True:
        delta = 0
        new_V = V.copy()
        for r in range(n):
            for c in range(n):
                state = (r, c)
                # Terminal state and obstacles stay 0
                if state == (end_r, end_c) or state in obs_list:
                    continue
                
                v_old = V[state]
                action = policy[f"{r},{c}"]
                dr, dc = actions[action]
                
                next_r, next_c = r + dr, c + dc
                if not (0 <= next_r < n and 0 <= next_c < n):
                    next_r, next_c = r, c
                
                reward = -1 # Step cost
                next_state = (next_r, next_c)
                
                # Bellman equation for fixed policy
                new_V[state] = reward + gamma * V[next_state]
                delta = max(delta, abs(v_old - new_V[state]))
        
        V = new_V
        iter_count += 1
        if delta < theta or iter_count > 1000:
            break
            
    return {f"{r},{c}": val for (r, c), val in V.items()}

def generate_random_policy(n):
    """
    Generate a random action for each state.
    """
    policy = {}
    possible_actions = ['U', 'D', 'L', 'R']
    for r in range(n):
        for c in range(n):
            policy[f"{r},{c}"] = random.choice(possible_actions)
    return policy

def value_iteration(n, end_pos, obstacles, gamma=0.9, theta=0.001):
    """
    Kept as an alternative or for reference.
    """
    V = {(r, c): 0.0 for r in range(n) for c in range(n)}
    end_r, end_c = map(int, end_pos.split(','))
    obs_list = [tuple(map(int, o.split(','))) for o in obstacles]
    actions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    while True:
        delta = 0
        new_V = V.copy()
        for r in range(n):
            for c in range(n):
                state = (r, c)
                if state == (end_r, end_c) or state in obs_list: continue
                v_old = V[state]
                action_values = []
                for action, (dr, dc) in actions.items():
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < n and 0 <= nc < n): nr, nc = r, c
                    action_values.append(-1 + gamma * V[(nr, nc)])
                new_V[state] = max(action_values)
                delta = max(delta, abs(v_old - new_V[state]))
        V = new_V
        if delta < theta: break
    policy = {}
    for r in range(n):
        for c in range(n):
            state = (r, c)
            if state == (end_r, end_c) or state in obs_list: policy[f"{r},{c}"] = ""; continue
            best_a = max(actions.keys(), key=lambda a: -1 + gamma * V[(r+actions[a][0], c+actions[a][1])] if 0<=r+actions[a][0]<n and 0<=c+actions[a][1]<n else -1 + gamma * V[(r,c)])
            policy[f"{r},{c}"] = best_a
    return {f"{r},{c}": val for (r, c), val in V.items()}, policy
