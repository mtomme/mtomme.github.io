from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from openai import OpenAI
import os

# Initialize Flask app
app = Flask(__name__)

#enable CORS
CORS(app)

# Set OpenAI API key from environment variable
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# List of available CSV file paths in the repository
AVAILABLE_CSV_FILES = {
    "ChevyCoupe": "Organized_Car_Data/Chevrolet/Coupe.csv" # Add more file paths as needed
    "AcuraCoupe": "Organized_Car_Data/Acura/Coupe.csv"
}

@app.route("/search", methods=["POST"])
def search_csv():
    """
    Endpoint to process a user query and search a selected CSV file.
    """
    try:
        # Get the user query and file ID from the JSON body
        data = request.get_json()
        user_query = data.get("user_query")
        file_id = data.get("file_id")

        # Check if the user query or file ID are missing
        if not user_query:
            return jsonify({"error": "User query is required"}), 400
        if not file_id:
            return jsonify({"error": "File identifier is required"}), 400

        # Check if the selected file exists in the available files
        file_path = AVAILABLE_CSV_FILES.get(file_id)
        if not file_path:
            return jsonify({"error": "Invalid file identifier or file not found"}), 404

        # Check if the file exists at the given path
        if not os.path.exists(file_path):
            return jsonify({"error": f"File not found at path: {file_path}"}), 404

        #print for debugging
        print(f"User query: {user_query}")
        print(f"File ID: {file_id}")

        # Read the CSV into a Pandas DataFrame
        pd.set_option('display.max_columns', None)
        csv = pd.read_csv(file_path, encoding='utf-8')

        print("CSV Read, sending prompt to ChatGPT...")

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

        # Return the result as JSON
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
