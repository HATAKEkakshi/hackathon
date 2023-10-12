// Set the countdown time to 10 minutes (600,000 milliseconds)
const countdownTime = 10 * 60 * 1000;

// Update the countdown every second
const countdown = setInterval(function() {
    const now = new Date().getTime();
    const timeRemaining = countdownTime - now;

    if (timeRemaining > 0) {
        const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

        document.getElementById('countdown').innerHTML = `${minutes}m ${seconds}s`;
    } else {
        document.getElementById('countdown').innerHTML = 'Time is up!';
        clearInterval(countdown);
    }
}, 1000);