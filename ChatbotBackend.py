from flask import Flask, request, jsonify
import pandas as pd
import openai
import os

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# List of available CSV file paths in the repository
AVAILABLE_CSV_FILES = {
    "ChevyCoupe": "Organized_Car_Data/Chevrolet/Coupe.csv" # Add more file paths as needed
}

@app.route("/search", methods=["POST"])
def search_csv():
    """
    Endpoint to process a user query and search a selected CSV file.
    """
    try:
        # Get the user query from the form data
        user_query = request.form.get("user_query")
        if not user_query:
            return jsonify({"error": "User query is required"}), 400

        # Get the selected file identifier from the request
        selected_file_id = request.form.get("file_id")
        if not selected_file_id:
            return jsonify({"error": "File identifier is required"}), 400

        # Check if the selected file exists in the available files
        file_path = AVAILABLE_CSV_FILES.get(selected_file_id)
        if not file_path:
            return jsonify({"error": "Invalid file identifier or file not found"}), 404

        # Check if the file exists at the given path
        if not os.path.exists(file_path):
            return jsonify({"error": f"File not found at path: {file_path}"}), 404

        # Read the CSV into a Pandas DataFrame
        pd.set_option('display.max_columns', None)
        csv = pd.read_csv(file_path, encoding='utf-8')

        # Construct the OpenAI prompt
        prompt = f"""
        You are an assistant that helps search through a car database.
        Here is the database:
        {csv}

        User Query: {user_query}
        Based on the above data, provide the most relevant rows or answers.
        """

        # Get response from ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an assistant that searches a CSV of cars."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract response content
        result = response.choices[0].message["content"]

        # Return the result as JSON
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
