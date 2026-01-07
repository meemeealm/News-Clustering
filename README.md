## News Clustering

## Problem Statement

This project tackles the challenge of **unsupervised categorization of news headlines**. Instead of predicting predefined labels, the model groups articles into clusters of related content. By applying NLP pipelines and ultimately selecting **Bisecting KMeans** as the clustering algorithm, the system breaks down large, dense “news blobs” into meaningful sub‑topics.

### What the model is predicting
- The model predicts **clusters of similar news articles** based on textual features extracted from headlines and short descriptions.  
- Each cluster represents a potential sub‑topic (e.g., politics, sports, technology, entertainment) discovered without human‑assigned labels.

### Who benefits
- **Readers**: Gain easier navigation through overwhelming volumes of news by seeing related stories grouped together.  
- **Journalists & editors**: Identify emerging themes or trending topics across large datasets.  
- **Researchers & analysts**: Use clusters to study media coverage patterns and topic evolution.  
- **News aggregators**: Improve personalization and recommendation systems by organizing content into coherent groups.

### How the model will be used
- Input: Raw news headlines and short descriptions.  
- Processing: Text preprocessing → TF‑IDF vectorization → dimensionality reduction → Bisecting KMeans clustering.  
- Output: Cluster assignments that group articles into sub‑topics.  
- These clusters can be visualized, analyzed, or used as a foundation for downstream tasks like topic labeling or recommendation engines.

### Why this problem matters
In today’s information‑dense environment, readers are flooded with thousands of articles daily. Without automated organization, valuable insights are buried in noise. **Unsupervised news clustering helps transform unstructured text into structured knowledge**, making it easier to digest, analyze, and act upon. This contributes to better information accessibility, improved media analysis, and more efficient content delivery.

---

### Pipeline

1. **Baseline Model**: Standard **K-Means** with default TF-IDF vectorization. This served as the primary benchmark for cluster separation and density.
2. **Tuned & Improved Models**: Optimized the TF-IDF "lens" by adjusting `max_df` (to ignore corpus-specific stop words) and implementing **Dimensionality Reduction (SVD)** and **Standard Scaling**.
* *Observation*: While these yielded "mathematically perfect" Silhouette scores (), they resulted in highly imbalanced clusters where the majority of data remained in a single "General News" group. 
3. **Bisecting K-Means (BiKMeans)**: Implemented a top-down hierarchical clustering approach.
* *Observation*: Even though the Silhouette score dropped to , this model successfully "shattered" the primary cluster, providing a much more even and semantically useful distribution of news topics.

<p align="center">
  <img src="images/workflow_news_clustering.png" width="20%" />
</p>

### Models Performance Comparison

The following table tracks the trade-off between mathematical tightness and cluster distribution:

| Metric | Baseline | Tuned | Improved Tuned | **BiKMeans** |
| --- | --- | --- | --- | --- |
| **Silhouette Score** | 0.554 | 0.783 | **0.800** | 0.562 |
| **Calinski-Harabasz** | 1227.8 | **2979.2** | 2802.1 | 620.8 |
| **Davies–Bouldin** | 0.643 | 0.471 | **0.316** | 2.396 |

---

### Tech Stack

* **Language**: Python
* **NLP**: Scikit-Learn (TF-IDF, SVD)
* **Clustering**: KMeans, BisectingKMeans
* **Visualization**: PCA (2D/3D), Matplotlib, Seaborn
* **Deployment**: Flask, Docker

---

### Model Selection & The "Optimization Paradox"

While the **Improved K-Means** model achieved the highest mathematical scores (, ), it suffered from the **"Majority Cluster Problem."** In this state, the model successfully isolated small niche topics (outliers) but failed to segment the core 90% of the dataset, leaving 40,000+ headlines in a single, uninformative "General News" blob.

![](images/clusters_comparison-min.png)  

![](images/clusters_tunedkmeans-min.png)  

![](images/clusters_bisectingkmeans-min.png)  


I  selected **Bisecting K-Means** as the production model for the following reasons:

* **Semantic Granularity:** By utilizing a hierarchical, top-down splitting strategy, BiKMeans forced the "General News" mass to fracture into distinct sub-topics (e.g., separating "Regional Politics" from "National Policy").
* **Balance vs. Separation:** A lower Silhouette score () in exchange for a lower **Gini Coefficient** (a measure of cluster size inequality).
* **Real-World Utility:** A model that provides 27 actionable, balanced categories is significantly more valuable for downstream tasks (like automated tagging or recommendation engines) than a model that provides one giant "Catch-all" category.

### Models Summary

| Model | Strategy | Primary Strength | Verdict |
| --- | --- | --- | --- |
| **K-Means Baseline** | Flat Clustering | Baseline performance | Weak distribution |
| **Improved Tuned** | SVD + Scaling | **Highest Math Scores** | Failed to segment core mass |
| **Bisecting K-Means** | Hierarchical Split | **Best Topic Discovery** | **Selected Model** |

---
### Setup & Installation

1. Clone the Repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Place the Model File
Ensure the trained pipeline file (`pipeline_bisecting.pkl`) is located in the project root (same folder as `app.py` or `serve.py`).

5. Run the Flask App
```bash
python app.py
```


```
http://127.0.0.1:5000/
```

6. Test in Browser (Form)
Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) and submit a headline + description via the form.

7. Test via Curl (Optional)
You can also test the `/predict` endpoint directly from bash:
```bash
curl -X POST http://127.0.0.1:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"headline":"Test Headline","short_description":"Test Description"}'
```
