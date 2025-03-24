from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Symptom-Disease Mapping
symptoms_data = {
    "fever": ["Viral Infection", "Flu", "COVID-19", "Malaria"],
    "cough": ["Common Cold", "Bronchitis", "Pneumonia", "COVID-19"],
    "headache": ["Migraine", "Tension Headache", "Sinusitis", "Dehydration"],
    "stomach pain": ["Food Poisoning", "Gastritis", "Appendicitis", "IBS"],
    "sore throat": ["Strep Throat", "Tonsillitis", "Laryngitis", "Viral Infection"],
    "fatigue": ["Anemia", "Thyroid Issues", "Chronic Fatigue Syndrome", "Diabetes"],
    "body pain": ["Viral Fever", "Fibromyalgia", "Muscle Strain", "Arthritis"],
    "chest pain": ["Heart Disease", "Acid Reflux", "Muscle Strain"],
    "shortness of breath": ["Asthma", "Pneumonia", "Anxiety", "Heart Problems"],
    "dizziness": ["Low Blood Pressure", "Vertigo", "Dehydration", "Anemia"],
    "vomiting": ["Food Poisoning", "Stomach Virus", "Pregnancy", "Motion Sickness"],
    "diarrhea": ["Food Poisoning", "IBS", "Bacterial Infection"],
}

@app.route('/')
def home():
    return render_template("index.html")  # Load chatbot UI

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    symptoms_input = data.get("symptoms", "").strip().lower()  # Normalize input

    # Split symptoms by comma
    input_symptoms = [s.strip() for s in symptoms_input.split(",") if s.strip()]

    matched_conditions = set()

    for symptom in input_symptoms:
        if symptom in symptoms_data:
            matched_conditions.update(symptoms_data[symptom])

    response = {
        "symptoms": input_symptoms,
        "possible_conditions": list(matched_conditions) if matched_conditions else ["No matching conditions found. Please consult a doctor."]
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
