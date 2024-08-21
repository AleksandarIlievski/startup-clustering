from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
import pandas as pd
import sys
sys.path.insert(0, '../../src/02 Data Preprocessing')
from src.DataPreprocessing.Preprocessing_en import preprocess_data
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans


def Create_tfidf_matrix(input_df):
    """
    Creates a Term Frequency-Inverse Document Frequency (TF-IDF) matrix based on the input DataFrame.

    Args:
        input_df (DataFrame): The input DataFrame containing website text data.

    Returns:
        tfidf_matrix (sparse matrix): The TF-IDF matrix representing the website text data.

    Dependencies:
        preprocess_data: A preprocessing function to clean and preprocess the website text data.
        TfidfVectorizer: A class from the scikit-learn library used for converting text documents into TF-IDF feature vectors.

    """
    df = input_df
    df['website_text_in_en'] = preprocess_data(df['website_text_in_en'])
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['website_text_in_en'])
    return tfidf_matrix

def Plot_Number_of_Cluster(tfidf_matrix):
    """
    Calculates connections between clusters based on the TF-IDF matrix and plots a dendrogram.

    Args:
        tfidf_matrix (sparse matrix): The TF-IDF matrix representing the text data.

    Returns:
        None: Displays the dendrogram.

    Dependencies:
        linkage: A function from the scipy.cluster.hierarchy module used for hierarchical clustering.
        dendrogram: A function from the scipy.cluster.hierarchy module used for plotting dendrograms.
        matplotlib.pyplot: A module for creating visualizations in Python.

    """
    # calculate connections between clusters
    linkage_matrix = linkage(tfidf_matrix.toarray(), method='ward')
    
    # plot dendogram
    plt.figure(figsize=(12, 6))
    dendrogram(linkage_matrix, truncate_mode='level')
    plt.xlabel('Texts')
    plt.ylabel('Distance')
    plt.title('Hierarchical Clustering dendrogram')
    plt.show()


def Create_Hierarchical_Clusters(df, tfidf_matrix, num_clusters):
    """
    Executes Hierarchical Clustering with the given number of clusters on the TF-IDF matrix.

    Args:
        df (DataFrame): The input DataFrame containing the text data.
        tfidf_matrix (sparse matrix): The TF-IDF matrix representing the text data.
        num_clusters (int): The desired number of clusters for the hierarchical clustering.

    Returns:
        df (DataFrame): The input DataFrame with an additional 'Cluster' column containing the cluster labels.

    Dependencies:
        AgglomerativeClustering: A class from the scikit-learn library used for hierarchical clustering.

    """
    # Execute Hierarchical Clustering with given number of clusters
    num_clusters = num_clusters
    clustering = AgglomerativeClustering(n_clusters=num_clusters)
    clustering.fit(tfidf_matrix.toarray())
    cluster_labels = clustering.labels_
    df['Cluster'] = cluster_labels
    return df


def Visualization_Hierarchical_Cluster(df, num_clusters):
    """
    Visualizes the clusters with word clouds based on the TF-IDF matrix.

    Args:
        df (DataFrame): The input DataFrame containing the text data and cluster labels.
        num_clusters (int): The number of clusters.

    Returns:
        None: Displays word clouds for each cluster.

    Dependencies:
        WordCloud: A class for generating word clouds.
        matplotlib.pyplot: A module for creating visualizations in Python.

    """
	# Visualize the clusters with Wordclouds
    for cluster in range(num_clusters):
        cluster_texts = df.loc[df['Cluster'] == cluster, 'website_text_in_en']


        # Plot relevant words of the cluster
        cluster_text = ' '.join(cluster_texts)
        wordcloud = WordCloud(collocations=False).generate(cluster_text)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"Cluster {cluster} Word Cloud")
        plt.show()
