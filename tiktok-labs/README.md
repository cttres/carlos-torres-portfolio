# 📱 TikTok Engagement & Content Classification – Machine Learning Workflow

### 🧠 Project Overview
This project simulates a real-world analytics workflow for TikTok’s data science team as part of the **Google Advanced Data Analytics Professional Certificate (Courses 2–6)**.  
It explores engagement behavior across user videos, identifies factors that drive visibility, and builds predictive models to classify videos and forecast engagement rates.

The project combines **Exploratory Data Analysis (EDA)**, **regression modeling**, and **machine learning classification** to demonstrate the full lifecycle of a data science solution — from data preparation to insight communication.

---

### 🎯 Objective
To understand which factors most influence video engagement (views, clicks, and watch time), and to build machine learning models that:
1. Predict engagement rate using regression analysis.  
2. Classify content as **claims vs. opinions** to support moderation and content triage.

---

### 📊 Dataset
- **Source:** Simulated TikTok dataset provided by Google Career Certificates  
- **Records:** Thousands of short-form video metrics  
- **Key Features:**  
  - `views`, `likes`, `clicks`, `watch_time`, `duration`  
  - `author_ban_status`, `verified_status`, `claim_status`  
- **Target Variables:**  
  - `engagement_rate` (regression)  
  - `claim_status` (classification)

---

### ⚙️ Methodology
#### 🧩 Data Preparation
- Handled missing values, duplicates, and outliers.  
- Engineered engagement metrics and standardized numeric fields.  
- Performed correlation analysis and visualized feature distributions.  

#### 🧮 Modeling and Analysis
1. **Exploratory Data Analysis (EDA):** Identified key engagement trends and skewed metrics.  
2. **Regression Modeling:**  
   - Built linear and multiple regression models to predict engagement rate.  
   - Achieved **R² > 0.85**, revealing strong influence of watch time and clicks.  
3. **Machine Learning Classification:**  
   - Trained Logistic Regression, Naïve Bayes, and Random Forest models.  
   - Final **Random Forest model achieved ~100% precision and ~99% recall**, offering high reliability for claim detection.  
   - Prioritized recall to minimize false negatives (missed claims).  

#### 🔍 Ethical Review
- Conducted bias and fairness assessment for features like author status and verification.  
- Proposed human-in-the-loop system to validate mid-confidence predictions.  

---

### 📈 Results & Insights
- **Top Engagement Drivers:** Watch time, click-through rate, and video duration.  
- **Claims vs. Opinions:** Claim videos received significantly higher engagement across all metrics.  
- **Best Model:** Random Forest Classifier with high generalization and interpretability.  
- **Business Impact:** Models enable faster triage, targeted moderation, and improved engagement strategy insights.  

---

### 🧰 Technologies Used
- **Languages & Tools:** Python, Jupyter Notebook  
- **Libraries:** Pandas, NumPy, Scikit-learn, Seaborn, Matplotlib  
- **Techniques:** Data Cleaning, EDA, Regression, Classification, Hyperparameter Tuning, Model Evaluation  

---

### 💬 Key Takeaways
This project demonstrates the end-to-end process of turning raw engagement data into actionable insights — integrating statistical analysis, model optimization, and ethical AI considerations. It reflects the practical workflow of a **Data Scientist or Machine Learning Engineer** working in social media analytics.

---

### 📊 Deliverables
- [📓 Course 2 Notebook](./Activity_Course%202%20TikTok%20project%20lab.ipynb)  
- [📓 Course 4 Notebook](./Activity_Course%204%20TikTok%20project%20lab.ipynb)  
- [📓 Course 5 Notebook](./Activity_Course%205%20TikTok%20project%20lab.ipynb)  
- [📓 Course 6 Notebook](./Activity_Course%206%20TikTok%20project%20lab.ipynb)

---

_This project was developed as part of the Google Advanced Data Analytics Professional Certificate, focusing on exploratory data analysis and regression modeling using TikTok engagement data._
