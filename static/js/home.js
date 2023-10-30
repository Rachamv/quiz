const startButton = document.getElementById("startButton");

function startQuiz() {
  const numQuestions = parseInt(
    document.getElementById("numQuestionsInput").value
  );
  if (numQuestions <= 0 || numQuestions > 100 || isNaN(numQuestions)) {
    alert("Please enter a valid number between 1 and 100.");
    return;
  }
  window.open("../templates/quiz.html", "_self");
}
