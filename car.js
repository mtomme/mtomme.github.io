document.addEventListener("DOMContentLoaded", () => {
    const startQuizBtn = document.getElementById("startQuizBtn");
    const quizSection = document.getElementById("quiz");

    startQuizBtn.addEventListener("click", () => {
        startQuizBtn.style.display = "none";
        quizSection.style.display = "block";
    });
});

function getRecommendation() {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "<p>Finding your perfect car...</p>";

    setTimeout(() => {
        resultsDiv.innerHTML = "<p>Your car recommendations will appear here.</p>";
    }, 1000);
}
