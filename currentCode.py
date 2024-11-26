import pandas as pd

class CarSelector:
    def __init__(self, data):
        self.data = data
        self.value_dict = self.build_value_dict()

    def build_value_dict(self):
        columns_of_interest = [
            'Make Name', 'Model Name', 'Trim Year', 'Engine Fuel Type', 'Engine Drive Type',
            'Body Type', 'Body Seats', 'Mileage Combined Mpg', 'Body Cargo Capacity'
        ]
        value_dict = {}
        for column in columns_of_interest:
            if column in self.data.columns:
                unique_values = self.data[column].dropna().unique().tolist()
                value_dict[column] = unique_values
        return value_dict

    def filter_cars(self, **filters):
        filtered_data = self.data
        if 'make' in filters:
            filtered_data = filtered_data[filtered_data['Make Name'].str.contains(filters['make'], case=False, na=False)]
        if 'model' in filters:
            filtered_data = filtered_data[filtered_data['Model Name'].str.contains(filters['model'], case=False, na=False)]
        if 'year' in filters:
            filtered_data = filtered_data[filtered_data['Trim Year'] == filters['year']]
        if 'max_price' in filters:
            max_price = filters['max_price']
            filtered_data = filtered_data[filtered_data['Trim Msrp'] <= max_price]
        if 'fuel_type' in filters:
            filtered_data = filtered_data[filtered_data['Engine Fuel Type'] == filters['fuel_type']]
        if 'drive_type' in filters:
            filtered_data = filtered_data[filtered_data['Engine Drive Type'] == filters['drive_type']]
        if 'body_type' in filters:
            filtered_data = filtered_data[filtered_data['Body Type'].str.contains(filters['body_type'], case=False, na=False)]
        if 'min_seats' in filters:
            filtered_data = filtered_data[filtered_data['Body Seats'] >= filters['min_seats']]
        if 'combined_mpg' in filters:
            filtered_data = filtered_data[filtered_data['Mileage Combined Mpg'] >= filters['combined_mpg']]
        if 'cargo_capacity' in filters:
            filtered_data = filtered_data[filtered_data['Body Cargo Capacity'] >= filters['cargo_capacity']]
        return filtered_data

def car_recommendation():
    file_path = '/home/mtomme/Downloads/carapi-opendatafeed-sample.csv'
    try:
        car_data = pd.read_csv(file_path)
        print("\nData loaded successfully.\n")
    except Exception as e:
        print("Error loading data:", e)
        return

    car_selector = CarSelector(car_data)

    while True:
        print("\nWelcome! Let’s find your ideal car by answering a few questions.\n")

        brand_preference = input("Preferred car brand (e.g., Toyota, Ford, BMW): ").strip().title()
        model_preference = input("Specific model? (Leave blank if any): ").strip().title()
        
        try:
            year_preference = int(input("Preferred model year (e.g., 2020, or press Enter if any): ").strip() or 0)
        except ValueError:
            year_preference = None

        try:
            max_price = int(input("What is your maximum budget? (Leave blank to skip): ").strip() or float('inf'))
        except ValueError:
            max_price = None

        print("\nFuel type options:", ', '.join(car_selector.value_dict.get('Engine Fuel Type', [])))
        fuel_type = input("Preferred fuel type: ").strip()
        if fuel_type and fuel_type not in car_selector.value_dict['Engine Fuel Type']:
            print(f"Invalid choice. Please choose from: {', '.join(car_selector.value_dict['Engine Fuel Type'])}")
            fuel_type = None

        print("\nDrive type options:", ', '.join(car_selector.value_dict.get('Engine Drive Type', [])))
        drive_type = input("Preferred drive type: ").strip()
        if drive_type and drive_type not in car_selector.value_dict['Engine Drive Type']:
            print(f"Invalid choice. Please choose from: {', '.join(car_selector.value_dict['Engine Drive Type'])}")
            drive_type = None

        print("\nBody type options:", ', '.join(car_selector.value_dict.get('Body Type', [])))
        body_type = input("Preferred body type: ").strip()
        if body_type and body_type not in car_selector.value_dict['Body Type']:
            print(f"Invalid choice. Please choose from: {', '.join(car_selector.value_dict['Body Type'])}")
            body_type = None

        try:
            min_seats = int(input("Minimum seats required: ").strip() or 0)
        except ValueError:
            min_seats = None

        try:
            combined_mpg = int(input("Minimum combined MPG: ").strip() or 0)
        except ValueError:
            combined_mpg = None

        try:
            cargo_capacity = int(input("Minimum cargo capacity (cubic feet): ").strip() or 0)
        except ValueError:
            cargo_capacity = None

        filters = {
            'make': brand_preference if brand_preference else None,
            'model': model_preference if model_preference else None,
            'year': year_preference,
            'max_price': max_price,
            'fuel_type': fuel_type,
            'drive_type': drive_type,
            'body_type': body_type,
            'min_seats': min_seats,
            'combined_mpg': combined_mpg,
            'cargo_capacity': cargo_capacity
        }
        filters = {k: v for k, v in filters.items() if v}

        car_data_filtered = car_selector.filter_cars(**filters)

        if not car_data_filtered.empty:
            print("\nRecommended cars based on your preferences:\n")
            print(car_data_filtered[['Make Name', 'Model Name', 'Trim Year', 'Body Type', 'Engine Fuel Type', 'Trim Msrp']].to_string(index=False))
        else:
            print("\nNo matches found based on your preferences. Try adjusting some options.\n")

        retry = input("\nWould you like to try again with different choices? (yes/no): ").strip().lower()
        if retry != 'yes':
            print("\nThank you for using the car recommendation service!")
            break

if __name__ == "__main__":
    car_recommendation()
