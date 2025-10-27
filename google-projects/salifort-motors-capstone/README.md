# 🧩 Employee Retention Prediction — Salifort Motors (Google Capstone Project)

### 📘 Project Overview
This project was developed as part of the **Google Advanced Data Analytics Professional Certificate** capstone.  
The objective was to help the HR department at **Salifort Motors** identify employees at risk of leaving by building a predictive model for employee turnover using machine learning techniques.

We explored, trained, and evaluated multiple classification models — **Random Forest** and **XGBoost** — to determine which provided the best balance between interpretability and predictive performance.

---

### 🧠 Objective
To create a reliable and explainable model that predicts employee turnover and provides actionable insights to improve retention and workforce satisfaction.

---

### 📊 Dataset
- **Source:** Provided in the Google Capstone dataset  
- **Records:** 15,000 employee entries  
- **Features:**  
  - Satisfaction level  
  - Last evaluation  
  - Number of projects  
  - Average monthly hours  
  - Time spent at the company (tenure)  
  - Department, salary, and status  
- **Target:** `left` (1 = employee left, 0 = stayed)

---

### ⚙️ Methodology

#### 🧩 Data Preparation
- Handled missing values and standardized numeric columns  
- Encoded categorical variables (department, salary)  
- Split data into training and test sets (80/20)  
- Performed exploratory data analysis to identify correlations between workload, satisfaction, and turnover  

#### 🧮 Models Implemented

| Model | Description | Key Notes |
|--------|--------------|-----------|
| **Random Forest Classifier** | Ensemble model of decision trees | Tuned with `GridSearchCV` (216 candidates) |
| **XGBoost Classifier** | Gradient boosting algorithm | Tuned with 72 hyperparameter combinations |

---

### 📈 Results

| Metric | Random Forest | XGBoost |
|--------|----------------|----------|
| **Accuracy** | **0.985** | 0.972 |
| **Precision** | **0.992** | 0.984 |
| **Recall** | **0.917** | 0.902 |
| **F1-Score** | **0.953** | 0.943 |

**Key Insight:**  
The **Random Forest** model outperformed XGBoost, providing higher recall and interpretability — ideal for HR applications where false negatives (missed resignations) are costly.

---

### 💬 Discussion
- **Top predictors** of employee attrition included satisfaction level, last evaluation, number of projects, and workload.  
- Employees with **low satisfaction** and **high workloads** were significantly more likely to leave.  
- **Department trends:** Sales, Support, and Technical teams showed the highest turnover.  
- Model explainability was prioritized to support HR policy decisions rather than just predictive accuracy.

---

### 🧠 Conclusion
- **Best Model:** Random Forest Classifier  
- **Model Accuracy:** 98.5%  
- **Business Impact:** Enables HR teams to proactively identify at-risk employees and take preventive actions.  
- **Next Steps:** Integrate the model into HR dashboards, automate retraining, and track turnover trends over time.

---

### 🧰 Technologies Used
- **Python**
- **Pandas**, **NumPy**
- **Scikit-learn**
- **XGBoost**
- **Matplotlib**, **Seaborn**
- **GridSearchCV** (for hyperparameter tuning)

---

### 📊 Deliverables
- [📘 Executive Summary (PDF)](./Capstone%20Executive%20Summary.pdf)  
- [📓 Jupyter Notebook](./google-projects/salifort-motors-capstone/Employee_Retention_Model.ipynb)


_This project was developed as part of the Google Advanced Data Analytics Professional Certificate capstone, focused on applying data-driven decision-making to real-world HR challenges._
