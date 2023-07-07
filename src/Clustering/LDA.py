import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from sklearn.decomposition import LatentDirichletAllocation as LDA
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from src.DataPreprocessing.Preprocessing_en import preprocess_data

def create_LDA_WordCloud(df, num_clusters):
    """
    Creates word clouds for each cluster in a dataset using Latent Dirichlet Allocation (LDA) clustering.

    Args:
        df (DataFrame): The input DataFrame containing the text data.
        num_clusters (int): The desired number of clusters for the LDA clustering.

    Returns:
        None: Displays word clouds for each cluster.

    Note:
        This function assumes that the input DataFrame 'df' contains a column named 'Content_in_de'
        that represents the preprocessed text data in German.

    """
    df.drop("Content", axis=1, inplace=True)
    df['Content_in_de'] = preprocess_data(df['Content_in_de'])

    # Erstelle den TF-IDF-Vektorizer
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,1), max_df=0.8, min_df=0.2)
    tfidf_matrix = vectorizer.fit_transform(df['Content_in_de'])

    # Führe das LDA Clustering durch
    num_clusters = num_clusters  # Anzahl der Cluster
    lda = LDA(n_components = num_clusters)
    lda_clustering = lda.fit_transform(tfidf_matrix.toarray())

    df['Cluster'] = np.argmax(lda_clustering, axis=-1).tolist()

    # Print texts for each cluster
    for cluster in range(num_clusters):
        cluster_texts = df.loc[df['Cluster'] == cluster, 'Content_in_de']

        # Plot relevant words of the cluster
        cluster_text = ' '.join(cluster_texts)
        wordcloud = WordCloud().generate(cluster_text)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"Cluster {cluster} Word Cloud")
        plt.show()