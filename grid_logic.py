import random

def policy_evaluation(n, start_pos, end_pos, obstacles, policy, gamma=0.9, theta=0.001):
    # Initialize V(s) = 0
    # positions are strings "r,c"
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
                # Terminal state and obstacles have value 0
                if state == (end_r, end_c) or state in obs_list:
                    continue
                
                v = V[state]
                action = policy[f"{r},{c}"]
                dr, dc = actions[action]
                
                next_r, next_c = r + dr, c + dc
                
                # Boundary check: stay in same cell if going out of bounds
                if not (0 <= next_r < n and 0 <= next_c < n):
                    next_r, next_c = r, c
                
                reward = -1 
                
                next_state = (next_r, next_c)
                new_V[state] = reward + gamma * V[next_state]
                
                delta = max(delta, abs(v - new_V[state]))
        
        V = new_V
        iter_count += 1
        if delta < theta or iter_count > 1000:
            break
            
    return {(f"{r},{c}"): val for (r, c), val in V.items()}

def generate_random_policy(n):
    policy = {}
    possible_actions = ['U', 'D', 'L', 'R']
    for r in range(n):
        for c in range(n):
            policy[f"{r},{c}"] = random.choice(possible_actions)
    return policy
