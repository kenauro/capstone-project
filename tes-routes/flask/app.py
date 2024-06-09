from flask import Flask, jsonify, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the pickled model from the local file system
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Endpoint to handle /predict
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the input data
        data = request.get_json()

        # List of expected input fields
        input_fields = [
            'booking_status', 'booking_guest_number', 'booking_currency', 'listing_id', 
            'review_sentiment', 'review_sentiment_score', 'booking_earned_in_idr', 'length_of_stay', 
            'seasonality', 'average_daily_rate', 'unit_id', 'bedroom', 'bathroom', 'beds', 'capacity', 
            'property_id', 'avg_daily_rate_per_unit', 'wifi', 'tv', 'cable_tv', 'ac', 'workspace', 'pool', 
            'parking', 'gym', 'kitchen', 'property_id1', 'area_id', 'area_name', 'area_distance_to_airport', 
            'airport_pickup_price_idr', 'booking_check_in_date', 'booking_check_in_month', 'booking_check_in_year', 
            'booking_check_out_date', 'booking_check_out_month', 'booking_check_out_year'
        ]

        # Convert the input data to a numpy array
        input_data = np.array([[data[field] for field in input_fields]])

        # Perform prediction using the loaded model
        prediction = model.predict(input_data)

        # Send the prediction back to the client
        return jsonify({
            'status': True,
            'code': 200,
            'message': 'OK',
            'data': {'booking_in_idr': prediction[0]}
        })

    except Exception as e:
        # Handle errors appropriately
        return jsonify({
            'status': False,
            'code': 500,
            'message': str(e),
            'data': None
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
