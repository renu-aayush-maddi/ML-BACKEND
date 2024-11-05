from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the trained model
model = pickle.load(open('ddos_model.sav', 'rb'))

@app.route('/')
def home():
    result = ''
    return render_template('index.html', result=result)

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    # Get input values from the form
    bwd_packet_length_mean = float(request.form['bwd_packet_length_mean'])
    bwd_packet_length_max = float(request.form['bwd_packet_length_max'])
    bwd_packet_length_std = float(request.form['bwd_packet_length_std'])
    avg_bwd_segment_size = float(request.form['avg_bwd_segment_size'])

    # Make prediction
    prediction = model.predict([[bwd_packet_length_mean, bwd_packet_length_max, bwd_packet_length_std, avg_bwd_segment_size]])[0]
    
    # Convert the predicted label back to original label name if necessary
    result = prediction  # Assuming the model output is already in label format

    return render_template('index.html', result='DDoS' if prediction == 1 else 'Normal')

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, request, jsonify
# import pickle

# app = Flask(__name__)

# # Load the model
# model = pickle.load(open('ddos_model.sav', 'rb'))

# @app.route('/')
# def home():
#     return "DDoS Prediction API is running"

# @app.route('/predict', methods=['POST'])
# def predict():
#     # Assume you receive JSON data
#     data = request.get_json()
#     input_data = [
#         data['bwd_packet_length_mean'],
#         data['bwd_packet_length_max'],
#         data['bwd_packet_length_std'],
#         data['avg_bwd_segment_size']
#     ]
#     prediction = model.predict([input_data])[0]
#     return jsonify({'prediction': 'DDoS' if prediction == 1 else 'Normal'})

# if __name__ == '__main__':
#     app.run()
