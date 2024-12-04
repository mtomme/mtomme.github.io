from flask import Flask, request, jsonify, session
from flask_cors import CORS
import pandas as pd
from openai import OpenAI
import os
import secrets

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

#enable CORS
CORS(app)

# Set OpenAI API key from environment variable
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# List of available CSV file paths in the repository
AVAILABLE_CSV_FILES = {
    "ChevyCoupe": "Organized_Car_Data/Chevrolet/Coupe.csv" # Add more file paths as needed
}

@app.route("/select_csv", methods=["POST"])
def select_csv():
    """
    Endpoint to set the selected CSV file in the user session.
    """
    try:
        data = request.get_json()
        file_id = data.get("file_id")

        if not file_id:
            return jsonify({"success": False, "error": "File identifier is required"}), 400

        # Check if the selected file exists in the available files
        file_path = AVAILABLE_CSV_FILES.get(file_id)
        if not file_path:
            return jsonify({"success": False, "error": "Invalid file identifier or file not found"}), 404

        # Save the selected file in the session
        session["selected_file"] = file_id
        return jsonify({"success": True, "message": f"File '{file_id}' selected successfully!"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/search", methods=["POST"])
def search_csv():
    """
    Endpoint to process a user query and search the selected CSV file.
    """
    try:
        # Get the user query from the JSON body
        data = request.get_json()
        user_query = data.get("user_query")

        if not user_query:
            return jsonify({"error": "User query is required"}), 400

        # Get the selected file from the session
        file_id = session.get("selected_file")
        if not file_id:
            return jsonify({"error": "No file selected. Please select a file first."}), 400

        # Check if the selected file exists in the available files
        file_path = AVAILABLE_CSV_FILES.get(file_id)
        if not file_path or not os.path.exists(file_path):
            return jsonify({"error": "Selected file not found."}), 404

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
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an assistant that searches a CSV of cars."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract response content
        result = response.choices[0].message.content
        print(result)

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
