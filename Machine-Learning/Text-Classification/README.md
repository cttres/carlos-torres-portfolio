# 📰 News Classification — Machine vs. Deep Learning Models

### 📘 Project Overview
This project evaluates the performance of **machine learning** and **deep learning** models in classifying TV news articles into predefined categories.  
We compared four models — **Random Forest**, **Support Vector Machine (SVM)**, **Long Short-Term Memory (LSTM)**, and **BERT** — to determine which achieves the highest accuracy and generalization in a multi-class text classification task.

---

### 🧠 Objective
To design and compare multiple text classification approaches (ML and DL) for accurately categorizing news articles into **Sport, Business, Politics, Tech,** and **Entertainment**.

---

### 📊 Dataset
- **Source:** TV news text dataset  
- **Instances:** 2,225 news articles  
- **Attributes:**  
  - `data`: textual content  
  - `labels`: category label  
- **Classes:**  
  - Sport (511), Business (510), Politics (417), Tech (401), Entertainment (386)

---

### ⚙️ Methodology

#### 🧩 Preprocessing
- Removed punctuation and special characters  
- Tokenization and lemmatization  
- TF-IDF vectorization for traditional ML models  
- Label encoding for categorical targets  
- For deep learning: used token embeddings and padded sequences  

#### 🧮 Models Implemented

| Model | Type | Description |
|--------|------|-------------|
| **Random Forest** | Machine Learning | Trained with 100 estimators; evaluated precision, recall, and F1-score per class. |
| **SVM (Linear Kernel)** | Machine Learning | Used `kernel='linear'`; delivered strong baseline performance. |
| **LSTM** | Deep Learning | Two-layer recurrent neural network with dropout (0.5), trained for 10 epochs. |
| **BERT (DistilBERT)** | Transformer Model | Fine-tuned with learning rate `5e-5`, 3 epochs, and CrossEntropyLoss. |

---

### 📈 Results

#### 📊 Class-wise F1-scores

| Model | Avg. F1-score | Accuracy | Runtime (s) |
|--------|----------------|-----------|-------------|
| **SVM** | 0.97 | 96.5% | 4.81 |
| **Random Forest** | 0.96 | 96.4% | 1.21 |
| **LSTM** | 0.97 | 96.8% | 16.53 |
| **BERT (DistilBERT)** | **0.99** | **98.5%** | 503.94 |

**Key Insight:**  
All models achieved strong results, but **BERT** significantly outperformed the others in accuracy and robustness, confirming the power of transformer-based models for text classification.

---

### 💬 Discussion
- **BERT** achieved the highest accuracy but required the longest runtime due to its complexity.  
- **LSTM** provided competitive performance with faster training times.  
- **SVM** and **Random Forest** served as strong baselines and required less computational power.  
- Preprocessing and text vectorization played a major role in improving model quality.

---

### 🧠 Conclusion
- **Best Model:** BERT (98.5% accuracy, F1-score 0.99)  
- **Key Takeaway:** Transformer models like BERT excel at understanding semantic context in short text documents.  
- **Future Work:** Further optimize hyperparameters, expand dataset size, and explore fine-tuning other transformer architectures (RoBERTa, DistilBERT).

---

### 🧰 Technologies Used
- **Python**
- **NumPy**, **Pandas**, **Scikit-learn**
- **TensorFlow / Keras**
- **PyTorch**, **Transformers (HuggingFace)**
- **Matplotlib**, **Seaborn**

_This project was developed collaboratively as part of a comparative study on deep learning and NLP classification, inspired by prior academic research on text classification and transformer-based models._
