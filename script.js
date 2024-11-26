let currentStep = 0;
let filters = {};
let quizSteps = [
    { question: "What car brand shall we start with?", type: "input", key: "make" },
    { question: "Pick a body type.", type: "options", key: "body_type", options: ["Sedan", "SUV", "Truck", "Coupe", "Convertible"] },
    { question: "What fuel type suits your needs?", type: "options", key: "fuel_type", options: ["Gasoline", "Diesel", "Electric", "Hybrid"] },
    { question: "Do you care about drive type?", type: "options", key: "drive_type", options: ["Front Wheel", "Rear Wheel", "All Wheel", "None"] }
];

const quizContainer = document.getElementById("quiz-container");
const questionEl = document.getElementById("question");
const answersEl = document.getElementById("answers");

function startQuiz() {
    currentStep = 0;
    filters = {};
    showQuestion();
}

function showQuestion() {
    const step = quizSteps[currentStep];
    questionEl.textContent = step.question;
    answersEl.innerHTML = "";

    if (step.type === "input") {
        answersEl.innerHTML = `<input type="text" id="input-${step.key}" placeholder="Type your answer...">`;
        answersEl.innerHTML += `<button onclick="nextQuestion('${step.key}')">Submit</button>`;
    } else if (step.type === "options") {
        step.options.forEach(option => {
            answersEl.innerHTML += `<button onclick="selectOption('${step.key}', '${option}')">${option}</button>`;
        });
    }
}

function nextQuestion(key) {
    const value = document.getElementById(`input-${key}`)?.value || filters[key];
    filters[key] = value || null;

    if (currentStep < quizSteps.length - 1) {
        currentStep++;
        showQuestion();
    } else {
        showResults();
    }
}

function selectOption(key, value) {
    filters[key] = value;
    nextQuestion(key);
}

function goBack() {
    if (currentStep > 0) {
        currentStep--;
        showQuestion();
    }
}

function startOver() {
    currentStep = 0;
    filters = {};
    showQuestion();
}

function showResults() {
    const resultText = document.getElementById("result-text");
    const filteredData = filterCars(filters); // Assuming you implement this function in JS
    resultText.textContent = filteredData.length ? `We found: ${filteredData[0].name}` : "No match found!";
    document.getElementById("result-container").style.display = "block";
    quizContainer.style.display = "none";
}

function filterCars(filters) {
    // Implement your CSV-based filtering here
    return [];
}

document.getElementById("startQuizBtn").addEventListener("click", () => {
    document.getElementById("quiz-container").style.display = "block";
    document.getElementById("startQuizBtn").style.display = "none";
    startQuiz();
});
