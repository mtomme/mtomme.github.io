from flask import Flask, request, jsonify, session
from flask_cors import CORS
import pandas as pd
from openai import OpenAI
import os
import secrets

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "c013e4b0fef5a665333ae1675e4198ec")
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

#enable CORS
CORS(app, supports_credentials=True)

# Set OpenAI API key from environment variable
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# List of available CSV file paths in the repository
AVAILABLE_CSV_FILES = {
    "AcuraCoupe": "Organized_Car_Data/Acura/Coupe.csv",
    "AcuraSedan": "Organized_Car_Data/Acura/Sedan.csv",
    "AcuraSUV": "Organized_Car_Data/Acura/SUV.csv",
    "AlfaRomeoCoupe": "Organized_Car_Data/Alfa Romeo/Coupe.csv",
    "AlfaRomeoSedan": "Organized_Car_Data/Alfa Romeo/Sedan.csv",
    "AlfaRomeoSUV": "Organized_Car_Data/Alfa Romeo/SUV.csv",
    "AstonMartinConvertible": "Organized_Car_Data/Aston Martin/Convertible.csv",
    "AstonMartinCoupe": "Organized_Car_Data/Aston Martin/Coupe.csv",
    "AstonMartinSedan": "Organized_Car_Data/Aston Martin/Sedan.csv",
    "AudiConvertible": "Organized_Car_Data/Audi/Convertible.csv",
    "AudiCoupe": "Organized_Car_Data/Audi/Coupe.csv",
    "AudiHatchback": "Organized_Car_Data/Audi/Hatchback.csv",
    "AudiSedan": "Organized_Car_Data/Audi/Sedan.csv",
    "AudiSUV": "Organized_Car_Data/Audi/SUV.csv",
    "AudiWagon": "Organized_Car_Data/Audi/Wagon.csv",
    "BentleyConvertible": "Organized_Car_Data/Bentley/Convertible.csv",
    "BentleyCoupe": "Organized_Car_Data/Bentley/Coupe.csv",
    "BentleySedan": "Organized_Car_Data/Bentley/Sedan.csv",
    "BentleySUV": "Organized_Car_Data/Bentley/SUV.csv",
    "BMWConvertible": "Organized_Car_Data/BMW/Convertible.csv",
    "BMWCoupe": "Organized_Car_Data/BMW/Coupe.csv",
    "BMWHatchback": "Organized_Car_Data/BMW/Hatchback.csv",
    "BMWSedan": "Organized_Car_Data/BMW/Sedan.csv",
    "BMWSUV": "Organized_Car_Data/BMW/SUV.csv",
    "BMWWagon": "Organized_Car_Data/BMW/Wagon.csv",
    "BuickConvertible": "Organized_Car_Data/Buick/Convertible.csv",
    "BuickHatchback": "Organized_Car_Data/Buick/Hatchback.csv",
    "BuickSedan": "Organized_Car_Data/Buick/Sedan.csv",
    "BuickSUV": "Organized_Car_Data/Buick/SUV.csv",
    "BuickWagon": "Organized_Car_Data/Buick/Wagon.csv",
    "CadillacCoupe": "Organized_Car_Data/Cadillac/Coupe.csv",
    "CadillacSedan": "Organized_Car_Data/Cadillac/Sedan.csv",
    "CadillacSUV": "Organized_Car_Data/Cadillac/SUV.csv",
    "ChevroletConvertible": "Organized_Car_Data/Chevrolet/Convertible.csv",
    "ChevroletCoupe": "Organized_Car_Data/Chevrolet/Coupe.csv",
    "ChevroletExtVan": "Organized_Car_Data/Chevrolet/Ext Van.csv",
    "ChevroletHatchback": "Organized_Car_Data/Chevrolet/Hatchback.csv",
    "ChevroletMinivan": "Organized_Car_Data/Chevrolet/Minivan.csv",
    "ChevroletSedan": "Organized_Car_Data/Chevrolet/Sedan.csv",
    "ChevroletSUV": "Organized_Car_Data/Chevrolet/SUV.csv",
    "ChevroletTruckCrewCab": "Organized_Car_Data/Chevrolet/Truck (Crew Cab).csv",
    "ChevroletTruckDoubleCab": "Organized_Car_Data/Chevrolet/Truck (Double Cab).csv",
    "ChevroletTruckExtendedCab": "Organized_Car_Data/Chevrolet/Truck (Extended Cab).csv",
    "ChevroletTruckRegularCab": "Organized_Car_Data/Chevrolet/Truck (Regular Cab).csv",
    "ChevroletVan": "Organized_Car_Data/Chevrolet/Van.csv",
    "ChryslerMinivan": "Organized_Car_Data/Chrysler/Minivan.csv",
    "ChryslerSedan": "Organized_Car_Data/Chrysler/Sedan.csv",
    "DodgeCoupe": "Organized_Car_Data/Dodge/Coupe.csv",
    "DodgeMinivan": "Organized_Car_Data/Dodge/Minivan.csv",
    "DodgeSedan": "Organized_Car_Data/Dodge/Sedan.csv",
    "DodgeSUV": "Organized_Car_Data/Dodge/SUV.csv",
    "FerrariConvertible": "Organized_Car_Data/Ferrari/Convertible.csv",
    "FerrariCoupe": "Organized_Car_Data/Ferrari/Coupe.csv",
    "FIATConvertible": "Organized_Car_Data/FIAT/Convertible.csv",
    "FIATHatchback": "Organized_Car_Data/FIAT/Hatchback.csv",
    "FIATSUV": "Organized_Car_Data/FIAT/SUV.csv",
    "FIATWagon": "Organized_Car_Data/FIAT/Wagon.csv",
    "FordCargoVan": "Organized_Car_Data/Ford/Cargo Van.csv",
    "FordConvertible": "Organized_Car_Data/Ford/Convertible.csv",
    "FordCoupe": "Organized_Car_Data/Ford/Coupe.csv",
    "FordExtVan": "Organized_Car_Data/Ford/Ext Van.csv",
    "FordHatchback": "Organized_Car_Data/Ford/Hatchback.csv",
    "FordMinivan": "Organized_Car_Data/Ford/Minivan.csv",
    "FordPassengerVan": "Organized_Car_Data/Ford/Passenger Van.csv",
    "FordSedan": "Organized_Car_Data/Ford/Sedan.csv",
    "FordSUV": "Organized_Car_Data/Ford/SUV.csv",
    "FordTruckCrewCab": "Organized_Car_Data/Ford/Truck (Crew Cab).csv",
    "FordTruckRegularCab": "Organized_Car_Data/Ford/Truck (Regular Cab).csv",
    "FordTruckSuperCab": "Organized_Car_Data/Ford/Truck (SuperCab).csv",
    "FordTruckSuperCrew": "Organized_Car_Data/Ford/Truck (SuperCrew).csv",
    "FordVan": "Organized_Car_Data/Ford/Van.csv",
    "FordWagon": "Organized_Car_Data/Ford/Wagon.csv",
    "GenesisSedan": "Organized_Car_Data/Genesis/Sedan.csv",
    "GMCExtVan": "Organized_Car_Data/GMC/Ext Van.csv",
    "GMCSUV": "Organized_Car_Data/GMC/SUV.csv",
    "GMCTruckCrewCab": "Organized_Car_Data/GMC/Truck (Crew Cab).csv",
    "GMCTruckDoubleCab": "Organized_Car_Data/GMC/Truck (Double Cab).csv",
    "GMCTruckExtendedCab": "Organized_Car_Data/GMC/Truck (Extended Cab).csv",
    "GMCTruckRegularCab": "Organized_Car_Data/GMC/Truck (Regular Cab).csv",
    "GMCVan": "Organized_Car_Data/GMC/Van.csv",
    "HondaCoupe": "Organized_Car_Data/Honda/Coupe.csv",
    "HondaHatchback": "Organized_Car_Data/Honda/Hatchback.csv",
    "HondaMinivan": "Organized_Car_Data/Honda/Minivan.csv",
    "HondaSedan": "Organized_Car_Data/Honda/Sedan.csv",
    "HondaSUV": "Organized_Car_Data/Honda/SUV.csv",
    "HondaTruckCrewCab": "Organized_Car_Data/Honda/Truck (Crew Cab).csv",
    "HyundaiCoupe": "Organized_Car_Data/Hyundai/Coupe.csv",
    "HyundaiHatchback": "Organized_Car_Data/Hyundai/Hatchback.csv",
    "HyundaiSedan": "Organized_Car_Data/Hyundai/Sedan.csv",
    "HyundaiSUV": "Organized_Car_Data/Hyundai/SUV.csv",
    "INFINITIConvertible": "Organized_Car_Data/INFINITI/Convertible.csv",
    "INFINITICoupe": "Organized_Car_Data/INFINITI/Coupe.csv",
    "INFINITISedan": "Organized_Car_Data/INFINITI/Sedan.csv",
    "INFINITISUV": "Organized_Car_Data/INFINITI/SUV.csv",
    "JaguarConvertible": "Organized_Car_Data/Jaguar/Convertible.csv",
    "JaguarCoupe": "Organized_Car_Data/Jaguar/Coupe.csv",
    "JaguarHatchback": "Organized_Car_Data/Jaguar/Hatchback.csv",
    "JaguarSedan": "Organized_Car_Data/Jaguar/Sedan.csv",
    "JaguarSUV": "Organized_Car_Data/Jaguar/SUV.csv",
    "JaguarWagon": "Organized_Car_Data/Jaguar/Wagon.csv",
    "JeepSUV": "Organized_Car_Data/Jeep/SUV.csv",
    "JeepTruckCrewCab": "Organized_Car_Data/Jeep/Truck (Crew Cab).csv",
    "KiaCoupe": "Organized_Car_Data/Kia/Coupe.csv",
    "KiaHatchback": "Organized_Car_Data/Kia/Hatchback.csv",
    "KiaMinivan": "Organized_Car_Data/Kia/Minivan.csv",
    "KiaSedan": "Organized_Car_Data/Kia/Sedan.csv",
    "KiaSUV": "Organized_Car_Data/Kia/SUV.csv",
    "KiaWagon": "Organized_Car_Data/Kia/Wagon.csv",
    "LamborghiniConvertible": "Organized_Car_Data/Lamborghini/Convertible.csv",
    "LamborghiniCoupe": "Organized_Car_Data/Lamborghini/Coupe.csv",
    "LamborghiniSUV": "Organized_Car_Data/Lamborghini/SUV.csv",
    "LandRoverSUV": "Organized_Car_Data/Land Rover/SUV.csv",
    "LexusConvertible": "Organized_Car_Data/Lexus/Convertible.csv",
    "LexusCoupe": "Organized_Car_Data/Lexus/Coupe.csv",
    "LexusHatchback": "Organized_Car_Data/Lexus/Hatchback.csv",
    "LexusSedan": "Organized_Car_Data/Lexus/Sedan.csv",
    "LexusSUV": "Organized_Car_Data/Lexus/SUV.csv",
    "LincolnSedan": "Organized_Car_Data/Lincoln/Sedan.csv",
    "LincolnSUV": "Organized_Car_Data/Lincoln/SUV.csv",
    "LincolnWagon": "Organized_Car_Data/Lincoln/Wagon.csv",
    "LotusCoupe": "Organized_Car_Data/Lotus/Coupe.csv",
    "MaseratiConvertible": "Organized_Car_Data/Maserati/Convertible.csv",
    "MaseratiCoupe": "Organized_Car_Data/Maserati/Coupe.csv",
    "MaseratiSedan": "Organized_Car_Data/Maserati/Sedan.csv",
    "MaseratiSUV": "Organized_Car_Data/Maserati/SUV.csv",
    "MazdaConvertible": "Organized_Car_Data/Mazda/Convertible.csv",
    "MazdaHatchback": "Organized_Car_Data/Mazda/Hatchback.csv",
    "MazdaMinivan": "Organized_Car_Data/Mazda/Minivan.csv",
    "MazdaSedan": "Organized_Car_Data/Mazda/Sedan.csv",
    "MazdaSUV": "Organized_Car_Data/Mazda/SUV.csv",
    "McLarenConvertible": "Organized_Car_Data/McLaren/Convertible.csv",
    "McLarenCoupe": "Organized_Car_Data/McLaren/Coupe.csv",
    "MercedesBenzConvertible": "Organized_Car_Data/Mercedes-Benz/Convertible.csv",
    "MercedesBenzCoupe": "Organized_Car_Data/Mercedes-Benz/Coupe.csv",
    "MercedesBenzExtVan": "Organized_Car_Data/Mercedes-Benz/Ext Van.csv",
    "MercedesBenzHatchback": "Organized_Car_Data/Mercedes-Benz/Hatchback.csv",
    "MercedesBenzMinivan": "Organized_Car_Data/Mercedes-Benz/Minivan.csv",
    "MercedesBenzSedan": "Organized_Car_Data/Mercedes-Benz/Sedan.csv",
    "MercedesBenzSUV": "Organized_Car_Data/Mercedes-Benz/SUV.csv",
    "MercedesBenzVan": "Organized_Car_Data/Mercedes-Benz/Van.csv",
    "MercedesBenzWagon": "Organized_Car_Data/Mercedes-Benz/Wagon.csv",
    "MINIConvertible": "Organized_Car_Data/MINI/Convertible.csv",
    "MINIHatchback": "Organized_Car_Data/MINI/Hatchback.csv",
    "MINIWagon": "Organized_Car_Data/MINI/Wagon.csv",
    "MitsubishiHatchback": "Organized_Car_Data/Mitsubishi/Hatchback.csv",
    "MitsubishiSedan": "Organized_Car_Data/Mitsubishi/Sedan.csv",
    "MitsubishiSUV": "Organized_Car_Data/Mitsubishi/SUV.csv",
    "NissanConvertible": "Organized_Car_Data/Nissan/Convertible.csv",
    "NissanCoupe": "Organized_Car_Data/Nissan/Coupe.csv",
    "NissanHatchback": "Organized_Car_Data/Nissan/Hatchback.csv",
    "NissanMinivan": "Organized_Car_Data/Nissan/Minivan.csv",
    "NissanSedan": "Organized_Car_Data/Nissan/Sedan.csv",
    "NissanSUV": "Organized_Car_Data/Nissan/SUV.csv",
    "NissanTruckCrewCab": "Organized_Car_Data/Nissan/Truck (Crew Cab).csv",
    "NissanTruckKingCab": "Organized_Car_Data/Nissan/Truck (King Cab).csv",
    "NissanTruckRegularCab": "Organized_Car_Data/Nissan/Truck (Regular Cab).csv",
    "NissanVan": "Organized_Car_Data/Nissan/Van.csv",
    "PolestarCoupe": "Organized_Car_Data/Polestar/Coupe.csv",
    "PorscheConvertible": "Organized_Car_Data/Porsche/Convertible.csv",
    "PorscheCoupe": "Organized_Car_Data/Porsche/Coupe.csv",
    "PorscheSedan": "Organized_Car_Data/Porsche/Sedan.csv",
    "PorscheSUV": "Organized_Car_Data/Porsche/SUV.csv",
    "PorscheWagon": "Organized_Car_Data/Porsche/Wagon.csv",
    "RamExtVan": "Organized_Car_Data/Ram/Ext Van.csv",
    "RamMinivan": "Organized_Car_Data/Ram/Minivan.csv",
    "RamTruckCrewCab": "Organized_Car_Data/Ram/Truck (Crew Cab).csv",
    "RamTruckMegaCab": "Organized_Car_Data/Ram/Truck (Mega Cab).csv",
    "RamTruckQuadCab": "Organized_Car_Data/Ram/Truck (Quad Cab).csv",
    "RamTruckRegularCab": "Organized_Car_Data/Ram/Truck (Regular Cab).csv",
    "RamVan": "Organized_Car_Data/Ram/Van.csv",
    "RollsRoyceConvertible": "Organized_Car_Data/Rolls-Royce/Convertible.csv",
    "RollsRoyceCoupe": "Organized_Car_Data/Rolls-Royce/Coupe.csv",
    "RollsRoyceSedan": "Organized_Car_Data/Rolls-Royce/Sedan.csv",
    "RollsRoyceSUV": "Organized_Car_Data/Rolls-Royce/SUV.csv",
    "ScionCoupe": "Organized_Car_Data/Scion/Coupe.csv",
    "ScionHatchback": "Organized_Car_Data/Scion/Hatchback.csv",
    "ScionSedan": "Organized_Car_Data/Scion/Sedan.csv",
    "ScionWagon": "Organized_Car_Data/Scion/Wagon.csv",
    "smartConvertible": "Organized_Car_Data/smart/Convertible.csv",
    "smartHatchback": "Organized_Car_Data/smart/Hatchback.csv",
    "SubaruCoupe": "Organized_Car_Data/Subaru/Coupe.csv",
    "SubaruHatchback": "Organized_Car_Data/Subaru/Hatchback.csv",
    "SubaruSedan": "Organized_Car_Data/Subaru/Sedan.csv",
    "SubaruSUV": "Organized_Car_Data/Subaru/SUV.csv",
    "TeslaSedan": "Organized_Car_Data/Tesla/Sedan.csv",
    "TeslaSUV": "Organized_Car_Data/Tesla/SUV.csv",
    "ToyotaCoupe": "Organized_Car_Data/Toyota/Coupe.csv",
    "ToyotaHatchback": "Organized_Car_Data/Toyota/Hatchback.csv",
    "ToyotaMinivan": "Organized_Car_Data/Toyota/Minivan.csv",
    "ToyotaSedan": "Organized_Car_Data/Toyota/Sedan.csv",
    "ToyotaSUV": "Organized_Car_Data/Toyota/SUV.csv",
    "ToyotaTruckAccessCab": "Organized_Car_Data/Toyota/Truck (Access Cab).csv",
    "ToyotaTruckCrewMax": "Organized_Car_Data/Toyota/Truck (CrewMax).csv",
    "ToyotaTruckDoubleCab": "Organized_Car_Data/Toyota/Truck (Double Cab).csv",
    "ToyotaTruckRegularCab": "Organized_Car_Data/Toyota/Truck (Regular Cab).csv",
    "ToyotaWagon": "Organized_Car_Data/Toyota/Wagon.csv",
    "VolkswagenConvertible": "Organized_Car_Data/Volkswagen/Convertible.csv",
    "VolkswagenHatchback": "Organized_Car_Data/Volkswagen/Hatchback.csv",
    "VolkswagenSedan": "Organized_Car_Data/Volkswagen/Sedan.csv",
    "VolkswagenSUV": "Organized_Car_Data/Volkswagen/SUV.csv",
    "VolkswagenWagon": "Organized_Car_Data/Volkswagen/Wagon.csv",
    "VolvoSedan": "Organized_Car_Data/Volvo/Sedan.csv",
    "VolvoSUV": "Organized_Car_Data/Volvo/SUV.csv",
    "VolvoWagon": "Organized_Car_Data/Volvo/Wagon.csv"
}

@app.route('/select_csv', methods=['POST'])
def select_csv():
    """
    Endpoint to set the selected CSV file in the user session.
    """
    try:
        data = request.get_json()
        make = data.get("make")
        body_type = data.get("body_type")

        if not make or not body_type:
            return jsonify({"success": False, "error": "Make and body type are required"}), 400

        # Create the key for the dictionary lookup
        key = f"{make}{body_type}"

        # Check if the key exists in the dictionary
        if key in AVAILABLE_CSV_FILES:
            csv_path = AVAILABLE_CSV_FILES[key]
            session["selected_file"] = key
            # Clear session history
            session["message_history"] = []
            return jsonify({"success": True, "csv_path": csv_path}), 200
        else:
            return jsonify({"success": False, "error": "CSV file not found for the provided make and body type"}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/chatbot", methods=["POST"])
def chatbot():
    """
    Endpoint to handle the chatbot interaction, keeping message history.
    """
    try:
        # Get the user query from the JSON body
        data = request.get_json()
        user_query = data.get("query")

        if not user_query:
            return jsonify({"error": "Query is required"}), 400

        # Initialize message history if it doesn't exist
        if "message_history" not in session:
            session["message_history"] = [
                {"role": "system", "content": "You are an assistant that helps search through a car database."}
            ]

        # Append the user's query to the message history
        session["message_history"].append({"role": "user", "content": user_query})

        # Get the selected file from the session
        file_id = session.get("selected_file")
        if not file_id:
            return jsonify({"error": "No file selected. Please select a file first."}), 400
        print(f"Selected File: {file_id}")

        # Check if the selected file exists in the available files
        file_path = AVAILABLE_CSV_FILES.get(file_id)
        if not file_path or not os.path.exists(file_path):
            return jsonify({"error": "Selected file not found."}), 404

        # Read the CSV into a Pandas DataFrame
        pd.set_option('display.max_columns', None)
        csv = pd.read_csv(file_path, encoding='utf-8')

        # Construct the OpenAI prompt based on the CSV data and user query
        prompt = f"""
            You are an assistant that helps users search through a car database in a friendly and conversational way. 

            Here is the car database (only relevant rows to the user's query will be used):

            {csv}

            User Query: {user_query}

            Your job is to:
            1. Provide a friendly greeting and acknowledge the user's query.
            2. Explain the search results in an easy-to-understand way, avoiding jargon.
            3. If the search results are broad or not specific enough, suggest ways the user could refine their query.
            4. Always be polite, helpful, and encourage further interaction. 

            Example of a friendly, helpful response format:
            - "Hi there! Here's what I found based on your query: [Results]"
            - "Based on what you're looking for, I found these options for you:"
            - If there are multiple results: "I found a few options for you, let me know if you need more details on any of them!"
            - If the results are not specific: "It looks like your search is a bit broad. You could try adding more details, like the model year or specific features you're looking for."

            When showing the search results, display them in the following format:
            - Model Name: [Model Name]
            - Trim Year: [Trim Year]
            - Trim Name: [Trim Name]
            - Trim MSRP: [Trim MSRP]
            - Engine Type: [Engine Type]
            - Engine Cylinders: [Engine Cylinders]
            - Mileage Combined Mpg: [Mileage Combined Mpg]
            - Body Doors: [Body Doors]
            - Body Seats: [Body Seats]

            Please avoid using Markdown formatting like bold or italics.
            
            Please return the response in a format that can be displayed properly on a website using HTML. 
        """

        # Add the prompt to the message history
        session["message_history"].append({"role": "system", "content": prompt})

        # Get response from ChatGPT using the message history
        response = client.chat.completions.create(
            model="gpt-4",
            messages=session["message_history"]
        )

        # Extract the response content
        result = response.choices[0].message.content
        print(result)

        # Append the assistant's response to the message history
        session["message_history"].append({"role": "assistant", "content": result})

        # Return the response
        return jsonify({"response": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_makes", methods=["GET"])
def get_makes():
    """
    Endpoint to get a list of car makes.
    """
    try:
        makes = list(set(key.split("/")[1] for key in AVAILABLE_CSV_FILES.values()))
        return jsonify({"success": True, "makes": sorted(makes)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/filter_by_make", methods=["POST"])
def filter_by_make():
    """
    Endpoint to filter files by car make.
    """
    try:
        data = request.get_json()
        make = data.get("make")

        if not make:
            return jsonify({"success": False, "error": "Make is required"}), 400

        # Filter files by make
        filtered_files = {
            key: value for key, value in AVAILABLE_CSV_FILES.items() if make in value
        }
        session["filtered_files"] = filtered_files

        return jsonify({"success": True, "message": f"Filtered by make '{make}' successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/get_body_types', methods=['GET'])
def get_body_types_by_make():
    """
    Retrieve a list of body types for a given car make.
    """
    make = request.args.get('make')

    if not make:
        return jsonify({"success": False, "error": "Make is required"}), 400

    # Extract body types for the specified make
    body_types = [
        key.replace(make, "").strip()  # Extract the body type from the dictionary key
        for key in AVAILABLE_CSV_FILES.keys()
        if key.startswith(make)
    ]

    if not body_types:
        return jsonify({"success": False, "error": f"No body types found for make: {make}"}), 404

    return jsonify({"success": True, "body_types": body_types}), 200


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
