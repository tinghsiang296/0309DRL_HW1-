let n = 5;
let startCell = null;
let endCell = null;
let obstacles = [];
let maxObstacles = n - 2;

const gridContainer = document.getElementById('grid-container');
const statusMsg = document.getElementById('status');
const gridNInput = document.getElementById('grid-n');
const resetBtn = document.getElementById('reset-btn');
const evaluateBtn = document.getElementById('evaluate-btn');

function initGrid() {
    n = parseInt(gridNInput.value);
    maxObstacles = n - 2;
    startCell = null;
    endCell = null;
    obstacles = [];
    
    gridContainer.style.gridTemplateColumns = `repeat(${n}, 60px)`;
    gridContainer.innerHTML = '';
    
    for (let r = 0; r < n; r++) {
        for (let c = 0; c < n; c++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.r = r;
            cell.dataset.c = c;
            cell.addEventListener('click', () => handleCellClick(r, c, cell));
            gridContainer.appendChild(cell);
        }
    }
    updateStatus();
}

function handleCellClick(r, c, cellElement) {
    const pos = `${r},${c}`;

    // 1. Set Start
    if (startCell === null) {
        startCell = pos;
        cellElement.classList.add('start');
        cellElement.innerHTML = 'Start';
    } 
    // 2. Set End
    else if (endCell === null) {
        if (pos === startCell) return;
        endCell = pos;
        cellElement.classList.add('end');
        cellElement.innerHTML = 'End';
    } 
    // 3. Set Obstacles (n-2)
    else if (obstacles.length < maxObstacles) {
        if (pos === startCell || pos === endCell || obstacles.includes(pos)) return;
        obstacles.push(pos);
        cellElement.classList.add('obstacle');
        cellElement.innerHTML = 'Obs';
    }
    
    updateStatus();
}

function updateStatus() {
    if (startCell === null) {
        statusMsg.innerText = 'Click a cell to set the START point (Green)';
    } else if (endCell === null) {
        statusMsg.innerText = 'Click a cell to set the END point (Red)';
    } else if (obstacles.length < maxObstacles) {
        statusMsg.innerText = `Click to set obstacles (${obstacles.length}/${maxObstacles})`;
    } else {
        statusMsg.innerText = 'Grid setup complete. Click "Evaluate Policy" to see values.';
    }
}

async function evaluatePolicy() {
    if (startCell === null || endCell === null || obstacles.length < maxObstacles) {
        alert('Please complete grid setup first (Start, End, and all Obstacles).');
        return;
    }

    const response = await fetch('/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            n: n,
            start: startCell,
            end: endCell,
            obstacles: obstacles
        })
    });

    const data = await response.json();
    displayResults(data.policy, data.values);
}

function displayResults(policy, values) {
    const cells = document.querySelectorAll('.cell');
    cells.forEach(cell => {
        const r = parseInt(cell.dataset.r);
        const c = parseInt(cell.dataset.c);
        const pos = `${r},${c}`;
        
        // Don't show policy/value on obstacles or end cell (terminal)
        if (obstacles.includes(pos) || pos === endCell) {
            return;
        }

        const action = policy[pos];
        const val = values[pos].toFixed(2);
        
        const arrowMap = { 'U': '↑', 'D': '↓', 'L': '←', 'R': '→' };
        
        cell.innerHTML = `
            <div class="arrow">${arrowMap[action] || ''}</div>
            <div class="value">${val}</div>
        `;
    });
}

resetBtn.addEventListener('click', initGrid);
evaluateBtn.addEventListener('click', evaluatePolicy);

// Initial load
initGrid();
