# mtomme.github.io
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Akinator-style AI to help users find the perfect car.">
    <title>Find Your Perfect Car</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }
        header {
            background-color: #333;
            color: #fff;
            padding: 20px;
            text-align: center;
        }
        header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        main {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 80vh;
            text-align: center;
        }
        .intro {
            max-width: 600px;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .intro h2 {
            font-size: 2em;
            margin-bottom: 20px;
        }
        .intro p {
            font-size: 1.2em;
            margin-bottom: 30px;
        }
        .start-btn {
            padding: 10px 20px;
            font-size: 1.2em;
            background-color: #333;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }
        .start-btn:hover {
            background-color: #555;
        }
        footer {
            text-align: center;
            padding: 10px;
            background-color: #333;
            color: #fff;
            position: fixed;
            width: 100%;
            bottom: 0;
        }
    </style>
</head>
<body>
    <header>
        <h1>Find Your Perfect Car</h1>
    </header>

    <main>
        <div class="intro">
            <h2>Discover the Car Made for You</h2>
            <p>Our AI, powered by a database from CarAPI, will guide you through a personalized selection process to find the perfect car.</p>
            <button class="start-btn" onclick="startQuiz()">Get Started</button>
        </div>
    </main>

    <footer>
        <p>Powered by CarAPI & AI</p>
    </footer>

    <script>
        function startQuiz() {
            // Redirect to the AI quiz page when ready
            window.location.href = 'quiz.html'; 
        }
    </script>
</body>
</html>
