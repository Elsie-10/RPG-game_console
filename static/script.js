const output = document.getElementById('game-output');
const startBtn = document.getElementById('start-btn');
const sendBtn = document.getElementById('send-btn');
const commandInput = document.getElementById('command-input');

// Function to append messages to output
function appendMessage(msg) {
    output.innerHTML += '<p>' + msg + '</p>';
}

// Start game
startBtn.addEventListener('click', async () => {
    try {
        const response = await fetch('/api/game/start', { method: 'POST' });
        const data = await response.json();
        appendMessage('Game started! Location: ' + data.data.location);
    } catch (error) {
        appendMessage('Error starting game: ' + error.message);
    }
});

// Send command
sendBtn.addEventListener('click', async () => {
    const command = commandInput.value.trim();
    if (!command) return;
    try {
        const response = await fetch('/api/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: command })
        });
        const data = await response.json();
        appendMessage('Response: ' + JSON.stringify(data));
    } catch (error) {
        appendMessage('Error sending command: ' + error.message);
    }
    commandInput.value = '';
});