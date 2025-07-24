# 🛒 Ecommerce Text Classification using LLM Embeddings

This notebook performs product text classification using embeddings generated from a SentenceTransformer model. It classifies ecommerce product descriptions into one of the four categories:

- 📚 **Books**  
- 👕 **Clothing & Accessories**  
- 🏠 **Household**  
- 📱 **Electronics**

### Workflow Summary
- Sentence embeddings are generated using a **task-specific model** from [SentenceTransformers](https://www.sbert.net/).
- Labels are encoded using **LabelEncoder**.
- A **machine learning classifier** is trained on the encoded embeddings to predict the product category.
- Model evaluation is performed using accuracy, precision, recall, F1 score, and a confusion matrix.

## 📘 Notebook and Dataset

<table>
  <tr>
    <td><strong>📔 View the Notebook</strong></td>
    <td>
      <a href="https://www.kaggle.com/code/arooshahmadds/ecommerce-text-classification" target="_blank">
        <img src="https://img.shields.io/badge/Open%20Notebook-Kaggle-blue?logo=kaggle" alt="Notebook Link">
      </a>
    </td>
  </tr>
  <tr>
    <td><strong>📦 Dataset Used</strong></td>
    <td>
      <a href="https://www.kaggle.com/datasets/saurabhshahane/ecommerce-text-classification" target="_blank">
        <img src="https://img.shields.io/badge/View%20Dataset-Kaggle-blue?logo=kaggle" alt="Dataset Link">
      </a>
    </td>
  </tr>
</table>

## 📁 Project Structure

```plaintext
ecommerce_text_classification/
│
├── 📘 ecommerce_text_classification.ipynb       # Full workflow notebook
├── 📂 embeddings_&_model/                       # Embedding generation and 
│   └── exommerce_text_classifier.pkl            # trained classifier 
│   └── text_embeddings.npy                      # Embedded Text
│   └── label_encodings.npy                      # Encoded Labels
│
├── 📄 README.md                                # Project overview (this file)
```

> ✨ Tip: You can modify the classifier head to experiment with models like Logistic Regression, SVM, RandomForest, or even fine-tuned transformer heads.
