from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

def policy_evaluation(n, start_pos, end_pos, obstacles, policy, gamma=0.9, theta=0.001):
    # Initialize V(s) = 0
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
                # Terminal state and obstacles have value 0 (or constant)
                if state == (end_r, end_c) or state in obs_list:
                    continue
                
                v = V[state]
                action = policy[f"{r},{c}"]
                dr, dc = actions[action]
                
                next_r, next_c = r + dr, c + dc
                
                # Boundary check: stay in same cell if going out of bounds
                if not (0 <= next_r < n and 0 <= next_c < n):
                    next_r, next_c = r, c
                
                # Reward: -1 for each step unless reaching goal? 
                # Or just basic evaluation. Let's use -1 per step, 0 at goal.
                reward = -1 
                
                next_state = (next_r, next_c)
                new_V[state] = reward + gamma * V[next_state]
                
                delta = max(delta, abs(v - new_V[state]))
        
        V = new_V
        iter_count += 1
        if delta < theta or iter_count > 1000:
            break
            
    return {(f"{r},{c}"): val for (r, c), val in V.items()}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    n = data['n']
    start = data['start']
    end = data['end']
    obstacles = data['obstacles']
    
    # Generate random policy for all non-terminal/non-obstacle cells
    policy = {}
    possible_actions = ['U', 'D', 'L', 'R']
    for r in range(n):
        for c in range(n):
            policy[f"{r},{c}"] = random.choice(possible_actions)
            
    values = policy_evaluation(n, start, end, obstacles, policy)
    
    return jsonify({
        'policy': policy,
        'values': values
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
