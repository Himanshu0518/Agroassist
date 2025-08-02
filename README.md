<p align="center">
  <img src="static/images/favicon.jpg" alt="AgroAssist Logo" width="120">
</p>

<h1 align="center">🌾 AgroAssist (किसान बंधु)</h1>

<p align="center">
  <b>Empowering Farmers with AI & ML for Smarter Agriculture</b>
</p>

<p align="center">
  <a href="#-features">Features</a> • 
  <a href="#-tech-stack">Tech Stack</a> • 
  <a href="#-methodology">Methodology</a> • 
  <a href="#-demo--screenshots">Demo</a> • 
  <a href="#-installation">Installation</a> • 
  <a href="#-about-the-author">Author</a> • 
  <a href="#-license">License</a>
</p>

---

## 🌟 Project Overview

**AgroAssist** is a smart agriculture assistant platform built to support farmers in making informed, data-driven decisions. It combines machine learning, deep learning, and real-time weather data to:

- Recommend the most profitable crops
- Detect plant diseases using leaf images
- Provide real-time farming suggestions and weather-based insights

---

## 🚀 Features

- ✅ **Crop Recommendation System**  
  Predicts the most profitable crop using:  
  *Profitability Score = (Predicted_Yield × Predicted_Price - Cost_of_Production) / Cost_of_Production*

- 🦠 **Plant Disease Detection**  
  Upload leaf images to identify diseases using CNN-based image classification.

- 🌤️ **Weather-Based Advisory**  
  Real-time weather insights for better planning and crop protection.

- 📝 **Farmer Expense Tracking**  
  Farmers can record expenses, manage budgets.

- 📝 **Farmer Blog Section**
   Farmers can view the blogs , post  blogs and can edit their own blog.

---

## 📂 Dataset
AgroAssist uses publicly shared datasets that have been curated, cleaned, and uploaded to Kaggle to support reproducibility and transparency.

| Dataset Name            | Description                                     |  
| ----------------------- | ----------------------------------------------- |
| **Crop Recommendation** | Soil & climate data for recommending best crops |                
| **Price Prediction**    | Historical market prices for various crops      |                
| **Yield Prediction**    | Crop-wise yield data with region information    |                
| **Disease Detection**   | Leaf images labeled with plant diseases         |                


---

## 🛠️ Tech Stack

| Layer               | Technology                                         |
|--------------------|-----------------------------------------------------|
| **Frontend**        | HTML, CSS, JavaScript                              |
| **Backend**         | Flask (Python Web Framework)                       |
| **Machine Learning**| Scikit-learn (Crop & Yield Prediction)             |
| **Deep Learning**   | TensorFlow / Keras (CNN for Plant Disease Detection)|
| **Forecasting**     | statsmodels.tsa (Time-Series Price Prediction)     |
| **Database**        | SQLite (for user data, blogs, expenses)            |
| **Visualization**   | Matplotlib, Seaborn                                |
| **Utilities**       | Pandas, NumPy                                      |

---

## 🧪 Methodology

AgroAssist applies a multi-model, AI-powered architecture:

- **Crop Recommendation Model**: Uses regression and classification models to predict the best crop based on:
  - Soil type
  - Weather forecast
  - Historical yield
  - Market price
  - Cost of production  
  - first on basis of soil parameters crop is recomended then for each crop profitability score is calculated to maximise net profit     considering less cost of production and high yield.

  **Profitability Score** = `(Yield_Predicted × Price_Predicted - Cost_of_Production) / Cost_of_Production`

- **Plant Disease Detection**:
  - Deep CNN trained on thousands of labeled plant disease images
  - Achieves high accuracy in real-time image classification

- **Weather-Based Advisory**:
  - Integrates live weather APIs
  - Offers suggestions like sowing time, irrigation needs, and pest risks

- **Blog & Finance Tracker**:
  - used quill.js to build blog section
  - SQLite for storing user data, expenses, blogs and income

---

## 📸 Demo 

🎥 **Watch the full walkthrough here**:  
[![AgroAssist Demo]](https://youtu.be/CQRa5K5qehQ)

---

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements or new features:

Fork the repo

Create a feature branch (git checkout -b feature-name)

Commit your changes (git commit -m 'Add feature')

Push to your branch (git push origin feature-name)

Create a pull request

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/Himanshu0518/Agroassist.git
cd agroassist

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Run the application
python app.py
```

---

👨‍💻 About the Author
Himanshu Singh

Aspiring Machine Learning Engineer & Data Scientist

Passionate about building real-world, impactful AI solutions

Proficient in MLOps, NLP, Deep Learning, and Data Engineering

GitHub | LinkedIn | Portfolio

I believe in solving problems that matter. AgroAssist was built to empower farmers, not just for a project, but for impact.

---

📄 License
This project is licensed under the MIT License.
Feel free to use, modify, and share with attribution.

<p align="center"> <i>“Technology should uplift those who grow our food.”</i> 🌾 </p> ```