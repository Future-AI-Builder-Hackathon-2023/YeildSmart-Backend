import pandas as pd
import pickle

dataset = pd.read_csv('crop_prediction.csv')

selected_features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

X = dataset[selected_features]

with open('crop_prediction.pkl', 'rb') as f:
    model = pickle.load(f)

X['temperature_mean'] = X['temperature'].mean()
X['humidity_std'] = X['humidity'].std()
X['rainfall_max'] = X['rainfall'].max()
X['temperature_humidity_interaction'] = X['temperature'] * X['humidity']
X['month'] = pd.to_datetime(dataset['date']).dt.month
X['season'] = pd.cut(X['month'], bins=[0, 3, 6, 9, 12], labels=['Winter', 'Spring', 'Summer', 'Autumn'])

rainfall_threshold = 100
humidity_threshold = 70

new_data = pd.DataFrame({
    'N': [25],
    'P': [50],
    'K': [40],
    'temperature': [28],
    'humidity': [75],
    'ph': [6.5],
    'rainfall': [100],
    'temperature_mean': [X['temperature'].mean()],
    'humidity_std': [X['humidity'].std()],
    'rainfall_max': [X['rainfall'].max()],
    'temperature_humidity_interaction': [28 * 75],
    'month': [6],
    'season': ['Summer']
})

predicted_outcome = model.predict(new_data)

pest_outbreak = False

if new_data['rainfall'].values[0] > rainfall_threshold and new_data['humidity'].values[0] > humidity_threshold:
    pest_outbreak = True

print("Predicted outcome:", predicted_outcome)
print("Pest outbreak possibility:", pest_outbreak)