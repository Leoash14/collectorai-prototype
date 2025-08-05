# 🧠 CollectorAI

AI-powered web app to identify, value, and manage collectibles like Hot Wheels, trading cards, and rare sneakers.

## 🎯 Features
- Upload an image and get collectible name
- Estimate item value (from mock eBay-style pricing)
- Save to your personal collection
- Simple and fully local demo (no API keys needed)

## 🛠️ Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python (Flask)
- AI Model: MobileNetV2 (transfer learning)
- Database: JSON (mock product data)

## 💻 How to Run Locally
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/collectorai.git
   cd collectorai

2. Install Python dependencies:

pip install -r requirements.txt


3. Run the Flask server:

python app.py


4. Open in browser:

http://localhost:5000



🗃️ Folder Structure

collectorai/
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   └── collection.html
├── app.py
├── model/
│   └── classifier_model.h5
├── data/
│   └── mock_prices.json
├── utils/
│   └── predict.py
└── README.md

🧠 AI Use

Pretrained MobileNetV2 model classifies uploaded images

Matches predictions to mock database of collectible items


🧸 Example Items

1968 Mazda Cosmo Sport (Hot Wheels)

Nike SB Dunk Low "Paris"

Mercedes-AMG Petronas F1 Car


🚀 Future Ideas

Real eBay API integration

Collection stats & value tracker

User login + profile

Price history charts



---

> Made for collectors, by a collector 🛠️🔥
