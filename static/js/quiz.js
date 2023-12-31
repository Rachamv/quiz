let currentQuestion = 0;
let quizData = [];

const quizContainer = document.getElementById("quizContainer");
const nextButton = document.getElementById("nextButton");
fetch("quiz.json")
  .then((response) => response.json())
  .then((data) => {
    quizData = data.results;
    currentQuestion = Math.floor(Math.random() * 100); // Select random question index between 0 and 99

    loadQuestion();
    // startButton.style.display = "none";
    nextButton.style.display = "block";
  })
  .catch((error) => console.error("Error fetching quiz data:", error));

function loadQuestion() {
  const question = quizData[currentQuestion];

  const questionElement = document.createElement("div");
  questionElement.innerHTML = `
                <h2>${question.category}</h2>
                <h3>${question.question}</h3>
            `;

  const answerOptions = document.createElement("div");
  question.incorrect_answers.push(question.correct_answer);
  question.incorrect_answers.sort();

  for (let i = 0; i < question.incorrect_answers.length; i++) {
    answerOptions.innerHTML += `
                    <input type="radio" name="answer" value="${question.incorrect_answers[i]}">
                    ${question.incorrect_answers[i]}<br>
                `;
  }

  questionElement.appendChild(answerOptions);
  quizContainer.innerHTML = "";
  quizContainer.appendChild(questionElement);
}

function loadNextQuestion() {
  const selectedAnswer = document.querySelector('input[name="answer"]:checked');
  if (!selectedAnswer) {
    alert("Please select an answer.");
    return;
  }

  // Handle the answer here if needed

  currentQuestion = Math.floor(Math.random() * 100); // Select another random question index
  loadQuestion();
}
