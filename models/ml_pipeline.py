import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, welch, find_peaks
import sklearn.preprocessing as prep
import json

class EGGSignalProcessor:
    """
    DSP Pipeline for Electrogastrogram (EGG) Signal Processing.
    EGG Normogastria band: 2.4 - 3.75 cpm (0.04 - 0.0625 Hz)
    Bradygastria band: 0.9 - 2.4 cpm (0.015 - 0.04 Hz)
    Tachygastria band: 3.75 - 10.0 cpm (0.0625 - 0.166 Hz)
    """
    def __init__(self, sampling_rate=2.0): # Default EGG sampling rate ~2 Hz
        self.fs = sampling_rate

    def bandpass_filter(self, signal, lowcut=0.015, highcut=0.2, order=3):
        nyq = 0.5 * self.fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        filtered = filtfilt(b, a, signal)
        return filtered

    def extract_features(self, raw_signal):
        filtered = self.bandpass_filter(raw_signal)
        
        # Power Spectral Density using Welch's Method
        freqs, psd = welch(filtered, fs=self.fs, nperseg=min(len(filtered), 256))
        freqs_cpm = freqs * 60.0  # Convert Hz to Cycles Per Minute (CPM)
        
        # Power bands in CPM
        brady_mask = (freqs_cpm >= 0.9) & (freqs_cpm < 2.4)
        normo_mask = (freqs_cpm >= 2.4) & (freqs_cpm <= 3.75)
        tachy_mask = (freqs_cpm > 3.75) & (freqs_cpm <= 10.0)
        
        total_power = np.sum(psd) + 1e-10
        brady_power = np.sum(psd[brady_mask]) / total_power
        normo_power = np.sum(psd[normo_mask]) / total_power
        tachy_power = np.sum(psd[tachy_mask]) / total_power
        
        dom_freq_idx = np.argmax(psd)
        dominant_freq_cpm = freqs_cpm[dom_freq_idx]
        
        peaks, _ = find_peaks(filtered, distance=self.fs*15) # Peak distance ~15s
        
        return {
            'bradygastria_power': float(brady_power),
            'normogastria_power': float(normo_power),
            'tachygastria_power': float(tachy_power),
            'dominant_frequency_cpm': float(dominant_freq_cpm),
            'mean_amplitude': float(np.mean(np.abs(filtered))),
            'std_amplitude': float(np.std(filtered)),
            'peak_count': int(len(peaks)),
            'filtered_signal': filtered.tolist(),
            'freqs_cpm': freqs_cpm.tolist(),
            'psd': psd.tolist(),
            'peaks': peaks.tolist()
        }

class DistilledStudentModel:
    """
    Simulates / Loads the compressed Student Model obtained via Knowledge Distillation.
    In production, load via tf.keras.models.load_model('student_model.h5')
    """
    def __init__(self):
        self.feature_names = [
            'bradygastria_power', 'normogastria_power', 'tachygastria_power',
            'dominant_frequency_cpm', 'mean_amplitude', 'std_amplitude', 'bmi', 'age'
        ]

    def predict(self, feature_dict):
        # Extract features vector
        normo = feature_dict['normogastria_power']
        tachy = feature_dict['tachygastria_power']
        brady = feature_dict['bradygastria_power']
        bmi = feature_dict.get('bmi', 24.0)
        
        # Clinical Rule-Informed ML Simulation (Mimicking Distilled Neural Network Softmax Outputs)
        # Low Normogastria + High Tachygastria/Bradygastria + High BMI -> Increased Risk
        risk_score = (1.0 - normo) * 0.4 + tachy * 0.3 + brady * 0.2 + (bmi / 40.0) * 0.1
        
        p_high = np.clip(risk_score ** 2, 0.02, 0.95)
        p_mod = np.clip(risk_score * 0.5, 0.03, 0.80)
        p_early = np.clip((1 - risk_score) * 0.4, 0.05, 0.70)
        p_healthy = np.clip(1.0 - (p_high + p_mod + p_early), 0.01, 0.95)
        
        probs = np.array([p_healthy, p_early, p_mod, p_high])
        probs /= np.sum(probs) # Softmax normalization
        
        classes = ['Healthy', 'Early Diabetes Risk', 'Moderate Diabetes Risk', 'High Diabetes Risk']
        pred_idx = np.argmax(probs)
        risk_level = classes[pred_idx]
        confidence = float(probs[pred_idx])
        
        # SHAP-like feature attributions
        shap_values = {
            'Normogastria Ratio': float((normo - 0.7) * -0.35),
            'Tachygastria Ratio': float((tachy - 0.1) * 0.28),
            'Bradygastria Ratio': float((brady - 0.15) * 0.22),
            'BMI Factor': float((bmi - 22.0) * 0.015),
            'Dominant Freq Shift': float((feature_dict['dominant_frequency_cpm'] - 3.0) * -0.12)
        }

        recommendations = {
            'Healthy': 'Maintain current diet and exercise routine. Standard annual follow-up recommended.',
            'Early Diabetes Risk': 'Schedule HbA1c screening. Initiate 30-day EGG re-evaluation and dietary counseling.',
            'Moderate Diabetes Risk': 'Order Fasting Plasma Glucose & OGTT. Refer to Endocrinology for autonomic evaluation.',
            'High Diabetes Risk': 'Immediate clinical intervention required. High probability of diabetic gastroparesis.'
        }

        return {
            'risk_level': risk_level,
            'confidence': confidence,
            'probabilities': {
                'healthy': float(probs[0]),
                'early': float(probs[1]),
                'moderate': float(probs[2]),
                'high': float(probs[3])
            },
            'shap_values': shap_values,
            'recommendation': recommendations[risk_level]
        }