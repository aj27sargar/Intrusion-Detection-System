

### ✅ Complete `README.md`:

```markdown
# 🚨 Network-Based Intrusion Detection System (NIDS)

This project is a Network-based Intrusion Detection System (NIDS) built using Python and anomaly detection techniques. It uses the KDDTrain+ dataset to detect suspicious or anomalous network activities and sends SMS alerts via Twilio when anomalies are found. The system also includes a Streamlit dashboard for real-time monitoring.

---

## 📁 Project Structure

```
Intrusion-Detection-System/
├── nids_dashboard.py          # Main Streamlit app
├── nids_model.py              # ML training and preprocessing
├── .env                       # Secret credentials (not pushed)
├── requirements.txt           # Required packages
└── README.md                  # Project guide
```

---

## 📦 Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

You can create a `requirements.txt` like:

```txt
pandas
numpy
scikit-learn
streamlit
twilio
python-dotenv
```

---

## 🧠 Dataset: KDDTrain+

We use the **KDDTrain+ dataset** from the NSL-KDD repository.

### 🔗 Download Dataset:

1. Visit: [https://www.unb.ca/cic/datasets/nsl.html](https://www.unb.ca/cic/datasets/nsl.html)
2. Scroll to **NSL-KDD** → Download `KDDTrain+.txt` and `KDDTest+.txt`
3. Place them in the project directory (or adjust path in code)

Alternatively, use `wget`:

```bash
wget https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain+.txt
wget https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest+.txt
```

---

## 🔍 Preprocessing & Model Training

To train and save the anomaly detection model:

```bash
python nids_model.py
```

- This script:
  - Loads `KDDTrain+.txt`
  - Encodes categorical features
  - Scales numerical features
  - Trains an Isolation Forest
  - Saves the model as `nids_model.pkl`

---

## 🧪 Running the NIDS Dashboard

Run the real-time dashboard with anomaly detection + SMS alerts:

```bash
streamlit run nids_dashboard.py
```

### Features:
- Upload live network data
- Detect anomalies
- View real-time anomaly count
- Sends SMS alert via Twilio when anomalies are detected

---

## 📲 Twilio SMS Integration

You will receive an SMS alert when anomalies are found.

### 🔧 Setup Twilio:

1. Create a free Twilio account: https://www.twilio.com/try-twilio
2. Get the following credentials:
   - `ACCOUNT_SID`
   - `AUTH_TOKEN`
   - Twilio Phone Number
3. Add your personal number to receive alerts

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
TWILIO_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE=+1234567890
TARGET_PHONE=+919876543210
```

> Make sure `.env` is added to `.gitignore` to avoid exposing secrets.

---

## ⚠️ Common Errors

| Error | Fix |
|------|-----|
| `A 'To' phone number is required` | Set `TARGET_PHONE` in `.env` |
| `Push blocked: Twilio SID detected` | Remove secrets and use `.env` |
| `ModuleNotFoundError` | Install missing packages via `pip` |

---

## 🙌 Credits

- **Dataset**: NSL-KDD (University of New Brunswick)
- **Libraries**: Scikit-learn, Pandas, Streamlit, Twilio
- **Author**: [Ajit Sargar](https://github.com/aj27sargar)

---

## 📸 Screenshot![image](https://github.com/user-attachments/assets/b718ec68-7c87-4ddd-a593-32425dcd579e)
![image](https://github.com/user-attachments/assets/cdcadeaf-459d-472a-92c6-90697f945f2d)


![NIDS Dashboard Screenshot](screenshot.png)

---

## 🛡️ Disclaimer

This is a demo project for academic/educational purposes and may not cover all edge cases in production-grade intrusion detection systems.

```
