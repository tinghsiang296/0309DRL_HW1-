def value_iteration(n, end_pos, obstacles, gamma=0.9, theta=0.001):
    """
    Perform Value Iteration to find optimal V(s) and optimal policy.
    Returns: (V, policy) where V is a dict of values and policy is a dict of actions.
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
                
                # V(s) = max_a [R + gamma * V(s')]
                action_values = []
                for action, (dr, dc) in actions.items():
                    next_r, next_c = r + dr, c + dc
                    if not (0 <= next_r < n and 0 <= next_c < n):
                        next_r, next_c = r, c
                    
                    reward = -1 # Step cost
                    next_state = (next_r, next_c)
                    action_values.append(reward + gamma * V[next_state])
                
                new_V[state] = max(action_values)
                delta = max(delta, abs(v_old - new_V[state]))
        
        V = new_V
        iter_count += 1
        if delta < theta or iter_count > 1000:
            break
            
    # Extract Policy
    policy = {}
    for r in range(n):
        for c in range(n):
            state = (r, c)
            if state == (end_r, end_c) or state in obs_list:
                policy[f"{r},{c}"] = ""
                continue
                
            best_action = None
            max_val = -float('inf')
            for action, (dr, dc) in actions.items():
                next_r, next_c = r + dr, c + dc
                if not (0 <= next_r < n and 0 <= next_c < n):
                    next_r, next_c = r, c
                
                val = -1 + gamma * V[(next_r, next_c)]
                if val > max_val:
                    max_val = val
                    best_action = action
            policy[f"{r},{c}"] = best_action

    return (
        {f"{r},{c}": val for (r, c), val in V.items()},
        policy
    )
