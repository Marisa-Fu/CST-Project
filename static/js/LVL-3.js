// Function to open the balance popup
function openPopup() {
  document.getElementById("popup").style.display = "flex";

  // Optionally fetch updated balance (only if connected to backend)
  fetch('/get_balance', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include'
  })
  .then(res => res.json())
  .then(data => {
      if (data.cash !== undefined && data.lives !== undefined) {
          document.getElementById('cash-display').textContent = `Cash: $${data.cash}`;
          document.getElementById('lives-display').textContent = `Lives: ${data.lives}`;
      } else {
          alert("Error fetching balance.");
      }
  })
  .catch(err => console.error("Balance fetch error:", err));
}

function closePopup() {
  document.getElementById("popup").style.display = "none";
}

function showLogoutPopup() {
  document.getElementById("logout-popup").style.display = "flex";
}

function confirmLogout(confirm) {
  document.getElementById("logout-popup").style.display = "none";
  if (confirm) {
      window.location.href = "/login; // Flask route (not 5500)
  }
}

// ====================== QUIZ LOGIC ==========================

// Quiz data
const quizData = [ /* your existing 10 questions, unchanged */ ];

// Quiz state variables
let currentQuestionIndex = 0;
let score = 0;
let userAnswers = [];
let quizStarted = false;
let quizEnded = false;
let timeLeft = 10;
let questionTimerInterval;
let countdownInterval;

// DOM Elements
const questionContainer = document.getElementById('question-container');
const resultsContainer = document.getElementById('results-container');
const finalScoreDisplay = document.getElementById('final-score');
const restartButton = document.getElementById('restart-button');
const messageContainer = document.getElementById('message-container');
const quizTitle = document.getElementById('quiz-title');
const countdownDisplay = document.getElementById('countdown');
const timerDisplay = document.getElementById('timer-seconds');
const resultsSummary = document.getElementById('results-summary').querySelector('tbody');

// Display the current question
function displayQuestion() {
  messageContainer.textContent = '';
  const current = quizData[currentQuestionIndex];

  const questionEl = document.createElement('h2');
  questionEl.className = 'text-xl font-semibold mb-4 text-center special-gothic';
  questionEl.innerHTML = current.question;

  const optionsEl = document.createElement('div');
  optionsEl.className = 'options-container';

  const options = Array.isArray(current.correctAnswer) ? [...current.options] : current.options;

  options.forEach(option => {
      const button = document.createElement('button');
      button.className = 'option-button';
      button.textContent = option;
      button.dataset.option = option;

      if (userAnswers[currentQuestionIndex] === option) {
          button.classList.add('selected');
      }

      button.addEventListener('click', () => handleOptionSelect(option));
      optionsEl.appendChild(button);
  });

  questionContainer.innerHTML = '';
  questionContainer.appendChild(questionEl);
  questionContainer.appendChild(optionsEl);

  startQuestionTimer();
}

// Handle answer selection
function handleOptionSelect(option) {
  userAnswers[currentQuestionIndex] = option;
  clearInterval(questionTimerInterval);

  const correct = quizData[currentQuestionIndex].correctAnswer;
  const isCorrect = Array.isArray(correct)
      ? correct.includes(option)
      : correct === option;

  if (isCorrect) score++;

  if (currentQuestionIndex < quizData.length - 1) {
      currentQuestionIndex++;
      timeLeft = 10;
      displayQuestion();
  } else {
      showResults();
  }
}

// Show final results
function showResults() {
  questionContainer.classList.add('hidden');
  resultsContainer.classList.remove('hidden');
  finalScoreDisplay.textContent = score;
  quizTitle.textContent = "Quiz Results";
  clearInterval(questionTimerInterval);
  displayQuizSummary();
}

function displayQuizSummary() {
  resultsSummary.innerHTML = '';
  quizData.forEach((question, index) => {
      const row = document.createElement('tr');
      const qCell = document.createElement('td');
      const uCell = document.createElement('td');
      const cCell = document.createElement('td');
      const rCell = document.createElement('td');

      qCell.textContent = question.question.replace(/<[^>]+>/g, '').slice(0, 80) + "...";
      uCell.textContent = userAnswers[index] || '-';
      cCell.textContent = Array.isArray(question.correctAnswer)
          ? question.correctAnswer.join(', ')
          : question.correctAnswer;

      const correct = Array.isArray(question.correctAnswer)
          ? question.correctAnswer.includes(userAnswers[index])
          : userAnswers[index] === question.correctAnswer;

      rCell.textContent = correct ? "Correct" : "Incorrect";
      rCell.style.color = correct ? "green" : "red";

      row.appendChild(qCell);
      row.appendChild(uCell);
      row.appendChild(cCell);
      row.appendChild(rCell);
      resultsSummary.appendChild(row);
  });
}

// Restart the quiz
function restartQuiz() {
  currentQuestionIndex = 0;
  score = 0;
  userAnswers = [];
  quizStarted = false;
  quizEnded = false;
  timeLeft = 10;
  countdownDisplay.textContent = '';
  resultsContainer.classList.add('hidden');
  questionContainer.classList.add('hidden');
  quizTitle.textContent = "Which Topic Are You Doing?";
  clearInterval(countdownInterval);
  startQuiz();
}
restartButton.addEventListener('click', restartQuiz);

// Start countdown timer
function startQuestionTimer() {
  timeLeft = 10;
  timerDisplay.textContent = `00:${timeLeft}`;
  clearInterval(questionTimerInterval);
  questionTimerInterval = setInterval(() => {
      timeLeft--;
      timerDisplay.textContent = `00:${timeLeft < 10 ? '0' : ''}${timeLeft}`;
      if (timeLeft <= 0) {
          clearInterval(questionTimerInterval);
          handleNextQuestion();
      }
  }, 1000);
}

function handleNextQuestion() {
  if (currentQuestionIndex < quizData.length - 1) {
      currentQuestionIndex++;
      timeLeft = 10;
      displayQuestion();
  } else {
      showResults();
  }
}

// Start quiz with countdown
function startQuiz() {
  if (!quizStarted) {
      let count = 3;
      countdownDisplay.textContent = count;
      questionContainer.classList.add('hidden');
      resultsContainer.classList.add('hidden');
      timerDisplay.classList.add('hidden');

      document.querySelectorAll('main > :not(#countdown)').forEach(el => el.style.display = 'none');

      countdownInterval = setInterval(() => {
          count--;
          countdownDisplay.textContent = count;
          if (count <= 0) {
              clearInterval(countdownInterval);
              countdownDisplay.textContent = '';
              quizStarted = true;
              document.querySelectorAll('main > :not(#countdown)').forEach(el => el.style.display = '');
              questionContainer.classList.remove('hidden');
              displayQuestion();
          }
      }, 1000);
  } else {
      timeLeft = 10;
      displayQuestion();
  }
}

// Auto-start the quiz when the page loads
startQuiz();
