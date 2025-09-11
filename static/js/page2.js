// Handles LED state updates on Page 2
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('button[onclick="updateLED(1)"]').addEventListener('click', function() {
        updateLED(1);
    });

    document.querySelector('button[onclick="updateLED(0)"]').addEventListener('click', function() {
        updateLED(0);
    });
});

function updateLED(state) {
    fetch('/update_led', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ led_state: state })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('LED state updated successfully');
            document.querySelector('#led-state').textContent = state === 1 ? 'ON' : 'OFF';
        } else {
            alert('Failed to update LED state');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to update LED state');
    });
}
