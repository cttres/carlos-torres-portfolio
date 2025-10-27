# 💹 Bitcoin Price Prediction — Comparative Analysis of Deep Learning Models

### 📘 Project Overview
This project explores the performance of different **machine learning and deep learning models** for predicting Bitcoin prices.  
We implemented and compared three models — **LSTM**, **GRU**, and **XGBoost** — to evaluate which model best captures temporal dependencies and price movement patterns in cryptocurrency markets.

---

### 🧠 Objective
To identify the most effective model for forecasting Bitcoin closing prices using historical data from **Yahoo Finance** and **Kaggle**, while comparing **deep learning (LSTM, GRU)** versus **traditional ML (XGBoost)** methods.

---

### 📊 Dataset
- **Source:** Yahoo Finance API (`yfinance`) and Kaggle.com  
- **Time Period:** January 2020 – December 2020  
- **Records:** ~600,000 daily price entries  
- **Features:**  
  - `Date`, `Open`, `High`, `Low`, `Volume (BTC)`, `Volume (USD)`  
- **Target:** `Close` (daily closing price)

---

### ⚙️ Methodology

#### 🧩 Data Preparation
- Performed exploratory data analysis and **Augmented Dickey-Fuller (ADF)** test to assess stationarity.  
- Scaled target variable and created train-test splits (80/20 for GRU and LSTM; 70/30 for XGBoost).  
- Applied standardization and time-ordered splits to preserve sequence structure.

#### 🧮 Models Implemented

| Model | Description | Key Details |
|--------|--------------|--------------|
| **GRU** | Gated Recurrent Unit | 1 GRU layer + linear layer, Adam optimizer, 20 epochs, adaptive LR scheduler |
| **LSTM** | Long Short-Term Memory | 3 stacked layers (50 units each), dropout 0.2, Adam optimizer, 10 epochs |
| **XGBoost** | Extreme Gradient Boosting | `n_estimators=200`, `max_depth=8`, `learning_rate=0.2`, binary classification target |

---

### 📈 Results

| Model | Metric | Result |
|--------|---------|--------|
| **GRU** | Test MSE | **1.93e-05** |
| **LSTM** | Test MSE | 2.34e-05 |
| **XGBoost** | Accuracy | 64.5% |
| **XGBoost** | F1 Score | 56.2% |

**Key Insight:**  
The **GRU model** outperformed both LSTM and XGBoost, achieving the lowest error and demonstrating superior ability to capture short-term dependencies in Bitcoin price movements.

---

### 💬 Discussion
- **GRU**’s efficiency and ability to handle short-term dependencies made it the most effective model.  
- **LSTM** performed well but required more tuning for optimal generalization.  
- **XGBoost**, while simpler and faster, struggled to capture the nonlinear dynamics of the cryptocurrency market.  
- The results reinforce the strength of **recurrent neural networks (RNNs)** for time-series forecasting in volatile domains.

---

### 🧩 Challenges & Learnings
- Managing large-scale time-series data and model optimization with limited epochs.  
- Understanding hyperparameter tuning and learning rate scheduling for recurrent models.  
- Comparing neural networks against gradient boosting techniques in non-stationary financial data.

---

### 🧠 Conclusion
- **Best Model:** GRU  
- **Performance Summary:** GRU (MSE: 1.93e-05) > LSTM (MSE: 2.34e-05) > XGBoost (Acc: 64.5%)  
- Future work includes hyperparameter tuning with **GridSearchCV**, longer training runs, and incorporating **macroeconomic or blockchain indicators** for richer predictions.

---

### 🧰 Technologies Used
- **Python**
- **NumPy**, **Pandas**
- **TensorFlow / Keras**
- **Scikit-learn**
- **XGBoost**
- **Matplotlib**, **Seaborn**
