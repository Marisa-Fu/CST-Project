  function openPopup() {
    document.getElementById("popup").style.display = "flex";
  }
  // This opens the life/cash system popup
  function closePopup() {
    document.getElementById("popup").style.display = "none";
  }
// This closes the popup
  function showLogoutPopup() {
    document.getElementById("logout-popup").style.display = "flex";
  }
  
  function confirmLogout(confirm) {
    const popup = document.getElementById("logout-popup");
    popup.style.display = "none";
  // This opens the Logout popup option
    if (confirm) {
      // Either you logout or u stay
      alert("You have been logged out.");
      // window.location.href = "/login"; // Optional redirect
    }
 
  }
  function startQuiz() {
    document.getElementById('start-container').style.display = 'none';
    // This gives us the "Start" button (container)
    const countdownWrapper = document.getElementById('countdown');
    const countdownNumber = document.getElementById('countdown-number');
    
    countdownWrapper.style.display = 'flex';
    countdownNumber.textContent = '3'; // Set the initial number first
  
    // Short delay to let the browser render the "3"
    setTimeout(() => {
      let count = 3;
      const countdown = setInterval(() => {
        count--;
        if (count > 0) {
          countdownNumber.textContent = count;
        } else {
          clearInterval(countdown);
          countdownWrapper.style.display = 'none';
          document.getElementById('quiz-container').style.display = 'block';
        }
      }, 1000);
    }, 100);
  }
  
 
  function checkAnswer(answer) {
    // Simple example of answer checking
    if (answer === 'D') {
      alert('Correct! Python is a programming language!');
    } else {
      alert('Incorrect, try again!');
    }
  }