# 📱 TikTok Engagement Analysis — Exploratory Data Analysis & Regression Modeling

### 📘 Project Overview
This project was completed as part of the **Google Advanced Data Analytics Professional Certificate** (Courses 2–6).  
It simulates a real-world analytics workflow for the **TikTok marketing team**, exploring engagement patterns across user videos, analyzing content performance, and applying regression techniques to predict engagement rates.

The goal was to build reproducible Python notebooks that apply **data cleaning, EDA, visualization, and statistical modeling** to uncover the key factors driving engagement on the TikTok platform.

---

### 🧠 Objective
To identify which variables — such as view count, clicks, and watch time — most influence **video engagement rates**, and to apply regression analysis to predict performance outcomes.

---

### 📊 Dataset
- **Source:** Simulated TikTok dataset (Google Career Certificate)  
- **Records:** Thousands of short-form video metrics  
- **Features:** `video_id`, `views`, `likes`, `clicks`, `watch_time`, `duration`, and categorical metadata  
- **Target Variable:** `engagement_rate` (calculated as clicks ÷ views)

---

### ⚙️ Methodology

#### 🧩 Data Preparation
- Checked for missing values, duplicates, and outliers  
- Cleaned and standardized numeric fields  
- Engineered engagement metrics from raw data  
- Visualized data distributions and relationships using **Seaborn** and **Matplotlib**

#### 🧮 Modeling & Analysis
- Applied **correlation analysis** to identify strongest predictors of engagement  
- Built **simple and multiple linear regression** models using **Scikit-learn**  
- Evaluated performance using **R²**, **MSE**, and **RMSE** metrics  
- Interpreted coefficients to understand how content metrics affect engagement

---

### 📈 Results
- Engagement was positively correlated with **watch time** and **number of clicks**  
- Regression models achieved strong explanatory power (**R² > 0.85**)  
- Visualizations revealed that shorter videos with consistent posting frequency often had higher engagement rates  
- Model coefficients provided actionable insights for content optimization

---

### 💬 Discussion
This project emphasized the complete **data analysis lifecycle** — from importing and cleaning data to communicating insights through visualizations and statistical evidence.  
The analysis reinforced how **regression modeling** can quantify the relationships between creator activity and audience engagement.

---

### 🧠 Conclusion
- **Key Findings:** Watch time and click-through rate are the most impactful engagement drivers  
- **Tools Used:** Python, Pandas, Seaborn, Scikit-learn, Matplotlib  
- **Outcome:** Provided data-driven recommendations to help TikTok teams understand which factors improve content visibility and interaction

---

### 🧰 Technologies Used
- **Python**
- **NumPy**, **Pandas**
- **Seaborn**, **Matplotlib**
- **Scikit-learn**
- **Jupyter Notebook**

---

### 📊 Deliverables
- [📓 Course 2 Notebook](./Activity_Course%202%20TikTok%20project%20lab.ipynb)  
- [📓 Course 4 Notebook](./Activity_Course%204%20TikTok%20project%20lab.ipynb)  
- [📓 Course 5 Notebook](./Activity_Course%205%20TikTok%20project%20lab.ipynb)  
- [📓 Course 6 Notebook](./Activity_Course%206%20TikTok%20project%20lab.ipynb)

---

_This project was developed as part of the Google Advanced Data Analytics Professional Certificate, focusing on exploratory data analysis and regression modeling using TikTok engagement data._
