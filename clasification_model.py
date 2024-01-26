# -*- coding: utf-8 -*-
"""Clasification Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IKs-RMokz16AzdSeL-CDaMot1vffRyuK
"""

import numpy as np

from google.colab import drive
drive.mount('/content/drive')

file_path = '/content/drive/MyDrive/MASTER_DATA/Data_Application /Modulo2/X.npy'
loaded_data = np.load ('/content/drive/MyDrive/MASTER_DATA/Data_Application /Modulo2/X.npy')

from google.colab import drive
drive.mount('/content/drive')

# Get the number of rows and columns
num_rows, num_columns = loaded_data.shape

# Print the number of rows and columns
print("Number of rows:", num_rows)
print("Number of columns:", num_columns)

largest_in_first_column = np.max(loaded_data[:, 0])

# Print the result
print("Largest value in the first column:", largest_in_first_column)

# Problem 2 - Transform the data

processed_data = np.log2(loaded_data + 1)

# Find the largest value in the first column of the processed data
largest_in_first_column = np.max(processed_data[:, 0])

# Print the result
print("Largest value in the first column of processed data:", largest_in_first_column)

# Problem 3 - Principal Components and Explained Variance

import numpy as np
from sklearn.decomposition import PCA

# Create a PCA model for raw data
pca_raw = PCA()
pca_raw.fit(loaded_data)

# Create a PCA model for processed data
pca_processed = PCA()
pca_processed.fit(processed_data)

# Calculate the percentage of variance explained by the first principal component for raw data
explained_variance_ratio_raw = pca_raw.explained_variance_ratio_[0]

# Calculate the percentage of variance explained by the first principal component for processed data
explained_variance_ratio_processed = pca_processed.explained_variance_ratio_[0]

# Print the results
print("Percentage of variance explained by the first principal component for raw data:", explained_variance_ratio_raw)
print("Percentage of variance explained by the first principal component for processed data:", explained_variance_ratio_processed)

# Function to find the number of PCs needed to explain a given percentage of variance
def find_num_pcs_to_explain_variance(data, explained_variance_threshold):
    pca = PCA()
    pca.fit(data)
    explained_variance_ratio_cumulative = np.cumsum(pca.explained_variance_ratio_)
    num_pcs_to_explain_variance = np.argmax(explained_variance_ratio_cumulative >= explained_variance_threshold) + 1
    return num_pcs_to_explain_variance

# Define the desired explained variance threshold (e.g., 0.85 for 85%)
explained_variance_threshold = 0.85

# Find the number of PCs needed for both raw and processed data
num_pcs_raw = find_num_pcs_to_explain_variance(loaded_data, explained_variance_threshold)
num_pcs_processed = find_num_pcs_to_explain_variance(processed_data, explained_variance_threshold)

print("Number of PCs needed to explain {}% of variance for raw data: {}".format(
    explained_variance_threshold * 100, num_pcs_raw))
print("Number of PCs needed to explain {}% of variance for processed data: {}".format(
    explained_variance_threshold * 100, num_pcs_processed))

# Problem 4 -  Plotting without Visualization Technique

import matplotlib.pyplot as plt

# Extract the first and second columns
first_column = processed_data[:, 0]
second_column = processed_data[:, 1]

# Create a scatterplot
plt.figure(figsize=(6, 4))
plt.scatter(first_column, second_column, alpha=0.5)  # 'alpha' controls transparency

# Add labels and title
plt.xlabel("First Coordinate")
plt.ylabel("Second Coordinate")
plt.title("Scatterplot of Log-Transformed Data (First vs. Second Coordinate)")

# Show the plot
plt.grid(True)
plt.show()

# Problem 5 - PCA

# Create a PCA model to find the top two principal components
pca = PCA(n_components=2)
principal_components = pca.fit_transform(processed_data)

# Create a scatterplot of the projections onto the first two principal components
plt.figure(figsize=(7, 4))
plt.scatter(principal_components[:, 0], principal_components[:, 1], alpha=0.5)

# Add labels and title
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("Scatterplot of Data Projected onto the Top Two Principal Components")

# Show the plot
plt.grid(True)
plt.show()

# Problem 6 - MDS

from sklearn.manifold import MDS

# Create an MDS model to reduce data to 2 dimensions
mds = MDS(n_components=2)

# Fit the MDS model to your data and get the reduced representation
mds_result = mds.fit_transform(processed_data)

# Create a scatterplot of the MDS result
plt.figure(figsize=(7, 5))
plt.scatter(mds_result[:, 0], mds_result[:, 1], alpha=0.5)

# Add labels and title
plt.xlabel("Dimension 1 (MDS)")
plt.ylabel("Dimension 2 (MDS)")
plt.title("MDS Visualization of Data in Two Dimensions")

# Show the plot
plt.grid(True)
plt.show()

# Problem 7 - tSNE
from sklearn.manifold import TSNE

# Step 1: Project the data onto the top 50 principal components
pca = PCA(n_components=500)
pca_result = pca.fit_transform(processed_data)

# Step 2: Run T-SNE on the projected data with perplexity=40
tsne = TSNE(n_components=2, perplexity=40, random_state=42)
tsne_result = tsne.fit_transform(pca_result)

# Create a scatterplot of the T-SNE result
plt.figure(figsize=(5, 3))
plt.scatter(tsne_result[:, 0], tsne_result[:, 1], alpha=0.5)

# Add labels and title
plt.xlabel("Dimension 1 (T-SNE)")
plt.ylabel("Dimension 2 (T-SNE)")
plt.title("T-SNE Visualization of Data in Two Dimensions (Top 500 PCs)")

# Show the plot
plt.grid(True)
plt.show()

# Problem 8 - Visualizing K-means Clustering

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Step 1: Project the data onto the top 50 principal components
pca = PCA(n_components=50)
pca_result = pca.fit_transform(processed_data)

# Step 2: Run K-Means clustering with 5 clusters
kmeans = KMeans(n_clusters=5, random_state=42)
cluster_labels = kmeans.fit_predict(pca_result)

# Step 3: Standardize the PCA result for MDS and T-SNE
scaler = StandardScaler()
standardized_pca_result = scaler.fit_transform(pca_result)

# Step 4: Run MDS on the standardized PCA result
mds = MDS(n_components=2)
mds_result = mds.fit_transform(standardized_pca_result)

# Step 5: Run T-SNE on the standardized PCA result with perplexity=40
tsne = TSNE(n_components=2, perplexity=40, random_state=42)
tsne_result = tsne.fit_transform(standardized_pca_result)

# Create scatterplots with cluster colors
plt.figure(figsize=(18, 6))

# PCA Plot with Cluster Colors
plt.subplot(131)
for i in range(5):
    plt.scatter(pca_result[cluster_labels == i, 0], pca_result[cluster_labels == i, 1], label=f'Cluster {i + 1}', alpha=0.5)
plt.title("PCA Visualization with Cluster Colors")
plt.xlabel("Dimension 1 (PCA)")
plt.ylabel("Dimension 2 (PCA)")
plt.legend()

# MDS Plot with Cluster Colors
plt.subplot(132)
for i in range(5):
    plt.scatter(mds_result[cluster_labels == i, 0], mds_result[cluster_labels == i, 1], label=f'Cluster {i + 1}', alpha=0.5)
plt.title("MDS Visualization with Cluster Colors")
plt.xlabel("Dimension 1 (MDS)")
plt.ylabel("Dimension 2 (MDS)")
plt.legend()

# T-SNE Plot with Cluster Colors
plt.subplot(133)
for i in range(5):
    plt.scatter(tsne_result[cluster_labels == i, 0], tsne_result[cluster_labels == i, 1], label=f'Cluster {i + 1}', alpha=0.5)
plt.title("T-SNE Visualization with Cluster Colors")
plt.xlabel("Dimension 1 (T-SNE)")
plt.ylabel("Dimension 2 (T-SNE)")
plt.legend()

plt.tight_layout()
plt.show()

# Problem 9 - Elbow Method

from sklearn.cluster import KMeans

pca = PCA(n_components=50)
pca_result = pca.fit_transform(processed_data)

wgss_values = []

k_values = range(1, 11)

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(pca_result)
    wgss_values.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(k_values, wgss_values, marker='o')
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Within-Cluster Sum of Squares (WGSS)")
plt.title("Elbow Method for Optimal K")
plt.grid(True)

wgss_values

# Define the number of clusters (K)
k = 3

# Create the K-Means model with K=4
kmeans = KMeans(n_clusters=k, random_state=42)

# Fit the model to the data
kmeans.fit(processed_data)

# Get the WGSS (inertia) for K=4
wgss_at_k = kmeans.inertia_

# Print the WGSS value
print("WGSS (Inertia) at K:", wgss_at_k) #near 6 million

"""# New Section"""



# Problem 11

# Define the number of clusters (K)
k = 5

# Create and fit a K-Means model
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(processed_data)

# Assign cluster labels to data points
cluster_labels = kmeans.predict(processed_data)

# Create an array to store the cluster means
cluster_means = np.zeros((k, processed_data.shape[1]))  # Initialize to zeros

# Calculate the cluster means for each cluster
for i in range(k):
    cluster_points = processed_data[cluster_labels == i]  # Get data points in the cluster
    cluster_mean = np.mean(cluster_points, axis=0)  # Calculate the mean for the cluster
    cluster_means[i] = cluster_mean

# Visualize cluster means using PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(cluster_means)

# Visualize cluster means using MDS
mds = MDS(n_components=2)
mds_result = mds.fit_transform(cluster_means)

# Create scatterplots for PCA and MDS results
plt.figure(figsize=(12, 5))

# PCA Plot for Cluster Means
plt.subplot(121)
plt.scatter(pca_result[:, 0], pca_result[:, 1], c=range(k), cmap='viridis', marker='o', s=100)
plt.title("PCA Visualization of Cluster Means")
plt.xlabel("Dimension 1 (PCA)")
plt.ylabel("Dimension 2 (PCA)")

# MDS Plot for Cluster Means
plt.subplot(122)
plt.scatter(mds_result[:, 0], mds_result[:, 1], c=range(k), cmap='viridis', marker='o', s=100)
plt.title("MDS Visualization of Cluster Means")
plt.xlabel("Dimension 1 (MDS)")
plt.ylabel("Dimension 2 (MDS)")

plt.tight_layout()
plt.show()

# Problem 12 - What if We Did Not Transform Data

# Create a PCA model to find the top two principal components
pca = PCA(n_components=2)
principal_components = pca.fit_transform(loaded_data)

# Create a scatterplot of the projections onto the first two principal components
plt.figure(figsize=(7, 4))
plt.scatter(principal_components[:, 0], principal_components[:, 1], alpha=0.5)

# Add labels and title
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("Scatterplot of Data Projected onto the Top Two Principal Components")

# Show the plot
plt.grid(True)
plt.show()

# Create an MDS model to reduce data to 2 dimensions
mds = MDS(n_components=2)

# Fit the MDS model to your data and get the reduced representation
mds_result = mds.fit_transform(loaded_data)

# Create a scatterplot of the MDS result
plt.figure(figsize=(7, 5))
plt.scatter(mds_result[:, 0], mds_result[:, 1], alpha=0.5)

# Add labels and title
plt.xlabel("Dimension 1 (MDS)")
plt.ylabel("Dimension 2 (MDS)")
plt.title("MDS Visualization of Data in Two Dimensions")

# Show the plot
plt.grid(True)
plt.show()

# Step 1: Project the data onto the top 50 principal components
pca = PCA(n_components=50)
pca_result = pca.fit_transform(loaded_data)

# Step 2: Run T-SNE on the projected data with perplexity=40
tsne = TSNE(n_components=2, perplexity=40, random_state=42)
tsne_result = tsne.fit_transform(pca_result)

# Create a scatterplot of the T-SNE result
plt.figure(figsize=(5, 3))
plt.scatter(tsne_result[:, 0], tsne_result[:, 1], alpha=0.5)

# Add labels and title
plt.xlabel("Dimension 1 (T-SNE)")
plt.ylabel("Dimension 2 (T-SNE)")
plt.title("T-SNE Visualization of Data in Two Dimensions (Top 50 PCs)")

# Show the plot
plt.grid(True)
plt.show()

"""##PROBLEM 2"""

#Problem 2: Larger unlabeled subset (Written Report)

file_path_2 = '/content/drive/MyDrive/MASTER_DATA/Data_Application /Modulo2/p2_unsupervised/X.npy'
loaded_data_2 = np.load(file_path_2)

processed_data_2 = np.log2(loaded_data_2 + 1)

num_rows, num_columns = loaded_data_2.shape

print("Number of rows:", num_rows)
print("Number of columns:", num_columns)

# Find the largest value in the first column of the processed data
largest_in_first_column = np.max(processed_data_2[:, 0])

# Print the result
print("Largest value in the first column of processed data:", largest_in_first_column)

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


# Perform PCA
pca = PCA()
pca.fit(processed_data_2)

# Determine the number of principal components for 85% variance
explained_variance_ratio = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance_ratio)
n_components_85 = np.argmax(cumulative_variance >= 0.85) + 1

# Project your data onto the selected number of principal components
x_pca = pca.transform(processed_data_2)[:, :n_components_85]

# Visualize the PCA results
plt.figure(figsize=(8, 6))
plt.scatter(x_pca[:, 0], x_pca[:, 1], c='b', marker='o')
plt.title('PCA with 85% Variance Explained')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.grid(True)
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


# Perform T-SNE
tsne = TSNE(n_components=2, perplexity=30, random_state=42)  # You can adjust perplexity as needed
x_tsne = tsne.fit_transform(processed_data_2)

# Visualize the T-SNE results
plt.figure(figsize=(8, 6))
plt.scatter(x_tsne[:, 0], x_tsne[:, 1], c='b', marker='o')
plt.title('T-SNE Visualization')
plt.xlabel('T-SNE Dimension 1')
plt.ylabel('T-SNE Dimension 2')
plt.grid(True)
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

# Load and preprocess your dataset
file_path_2 = '/content/drive/MyDrive/MASTER_DATA/Data_Application /Modulo2/p2_unsupervised/X.npy'
loaded_data_2 = np.load(file_path_2)
processed_data_2 = np.log2(loaded_data_2 + 1)

# Perform K-Means clustering
num_clusters = 12  # You can adjust the number of clusters as needed
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
cluster_labels = kmeans.fit_predict(processed_data_2)

# Perform T-SNE
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
x_tsne = tsne.fit_transform(processed_data_2)

# Visualize the T-SNE plot with cluster colors
plt.figure(figsize=(8, 6))
for cluster in range(num_clusters):
    plt.scatter(x_tsne[cluster_labels == cluster, 0],
                x_tsne[cluster_labels == cluster, 1],
                label=f'Cluster {cluster + 1}', alpha=0.5)

plt.title("T-SNE Visualization with K-Means Clusters")
plt.xlabel("Dimension 1 (T-SNE)")
plt.ylabel("Dimension 2 (T-SNE)")
plt.legend()
plt.grid(True)
plt.show()

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

inertia = []

# Prueba diferentes valores de k
for k in range(1, 15):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(processed_data_2) # QUE DATA SERÍA?
    inertia.append(kmeans.inertia_)

# Grafica la suma de las distancias intra-cluster
plt.figure(figsize=(8, 6))
plt.plot(range(1, 15), inertia, marker='o')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Within-Cluster Sum of Squares')
plt.title('Elbow Method for Optimal K')
plt.grid(True)
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# Split data into training and validation sets SOBRE QUE DATA TRABAJAR processed_data_2?
X_train, X_valid, y_train, y_valid = train_test_split(processed_data_2, cluster_labels, test_size=0.2, random_state=42)

# Train a logistic regression model with L1 regularization
#logistic_reg = LogisticRegression(C=1.0, penalty='l1', solver='liblinear', multi_class='ovr', random_state=42)
#logistic_reg.fit(X_train, y_train)

# Train a logistic regression model with L2 regularization
logistic_reg = LogisticRegression(C=1.0, penalty='l2', solver='liblinear', multi_class='ovr', random_state=42)
logistic_reg.fit(X_train, y_train)

# Train a logistic regression model with Elastic Net regularization
#logistic_reg = LogisticRegression(C=1.0, penalty='elasticnet', l1_ratio=0.5, solver='saga', multi_class='ovr', random_state=42)
#logistic_reg.fit(X_train, y_train)

# Make predictions on the validation set
y_pred = logistic_reg.predict(X_valid)

# Calculate accuracy on the validation set (you can use other metrics as well)
accuracy = accuracy_score(y_valid, y_pred)

# Report the choice of regularization parameter and validation performance
print(f"Chosen Regularization Parameter (C): {1.0}")
print(f"Validation Accuracy: {accuracy}")

"""Select Features based on Model Coefficients:"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
import matplotlib.pyplot as plt

# Load your evaluation training data (p2_evaluation)
file_path_3 = '/content/drive/MyDrive/MASTER_DATA/Data_Application /Modulo2/p2_evaluation/X_train.npy'
loaded_data_3 = np.load(file_path_3)

X_evaluation_train = np.log2(loaded_data_3 + 1)


# Standardize the data (important for feature selection)
#scaler = StandardScaler()
#X_evaluation_train_std = scaler.fit_transform(X_evaluation_train)

# Get the absolute coefficients and their indices
coeff_abs = np.abs(logistic_reg.coef_).sum(axis=0)
top_100_feature_indices = np.argsort(coeff_abs)[-100:]

# Select the top 100 features
X_top_100_features = X_evaluation_train[:, top_100_feature_indices]

"""Random Features Baseline:

Select 100 random features as a baseline.
"""

# Select 100 random feature indices
random_feature_indices = np.random.choice(X_evaluation_train.shape[1], 100, replace=False)

# Select the random features
X_random_features = X_evaluation_train[:, random_feature_indices]

"""High-Variance Features Baseline:

Select 100 features with the highest variances as another baseline.
"""

# Calculate variances of all features
feature_variances = np.var(X_evaluation_train, axis=0)

# Get indices of top 100 features with highest variances
top_variance_feature_indices = np.argsort(feature_variances)[-100:]

# Select the high-variance features
X_high_variance_features = X_evaluation_train[:, top_variance_feature_indices]

"""valuate the Models:

Train logistic regression classifiers on the selected feature subsets and evaluate their performance on the evaluation test data.
"""

# Load your evaluation training data (p2_evaluation)
file_path_4 = '/content/drive/MyDrive/MASTER_DATA/Data_Application /Modulo2/p2_evaluation/X_test.npy'
loaded_data_4 = np.load(file_path_4)

X_evaluation_test = np.log2(loaded_data_4 + 1)

# Apply the same preprocessing to the evaluation test data
X_evaluation_test = np.log2(X_evaluation_test + 1)
#X_evaluation_test_std = scaler.transform(X_evaluation_test)

file_path_5 = '/content/drive/MyDrive/MASTER_DATA/Data_Application /Modulo2/p2_evaluation/y_train.npy'
y_evaluation_train = np.load(file_path_5)
file_path_6 = '/content/drive/MyDrive/MASTER_DATA/Data_Application /Modulo2/p2_evaluation/y_test.npy'
y_evaluation_test = np.load(file_path_6)
# Train and evaluate the logistic regression classifier on the top 100 selected features
logistic_regression_model_top100 = LogisticRegression(C=1.0, penalty='l2', solver='liblinear', random_state=42)
logistic_regression_model_top100.fit(X_top_100_features, y_evaluation_train)
accuracy_top100 = logistic_regression_model_top100.score(X_evaluation_test[:, top_100_feature_indices], y_evaluation_test)

# Train and evaluate the logistic regression classifier on random features
logistic_regression_model_random = LogisticRegression(C=1.0, penalty='l2', solver='liblinear', random_state=42)
logistic_regression_model_random.fit(X_random_features, y_evaluation_train)
accuracy_random = logistic_regression_model_random.score(X_evaluation_test[:, random_feature_indices], y_evaluation_test)

# Train and evaluate the logistic regression classifier on high-variance features
logistic_regression_model_highvariance = LogisticRegression(C=1.0, penalty='l2', solver='liblinear', random_state=42)
logistic_regression_model_highvariance.fit(X_high_variance_features, y_evaluation_train)
accuracy_highvariance = logistic_regression_model_highvariance.score(X_evaluation_test[:, top_variance_feature_indices], y_evaluation_test)

# Report the accuracies
print(f"Accuracy with Top 100 Features: {accuracy_top100}")
print(f"Accuracy with Random Features: {accuracy_random}")
print(f"Accuracy with High-Variance Features: {accuracy_highvariance}")

"""Compare Feature Variances:

You can plot histograms of feature variances for both the top 100 selected features and the high-variance features to compare their distributions.
"""

# Calculate variances for the top 100 selected features
top_100_feature_variances = np.var(X_top_100_features, axis=0)

# Plot histograms of feature variances
plt.figure(figsize=(10, 6))
plt.hist(top_100_feature_variances, bins=50, alpha=0.5, label='Top 100 Selected Features', color='blue')
plt.hist(feature_variances[top_variance_feature_indices], bins=50, alpha=0.5, label='High-Variance Features', color='red')
plt.xlabel('Variance')
plt.ylabel('Frequency')
plt.title('Distribution of Feature Variances')
plt.legend()
plt.show()

# Calculate variances for the top 100 selected features
top_100_feature_variances = np.var(X_top_100_features, axis=0)

# Calculate variances for the random features
random_feature_variances = np.var(X_random_features, axis=0)

# Plot histograms of feature variances for both top 100 and random features
plt.figure(figsize=(10, 6))
plt.hist(top_100_feature_variances, bins=50, alpha=0.5, label='Top 100 Selected Features', color='blue')
plt.hist(random_feature_variances, bins=50, alpha=0.5, label='Random Features', color='green')
plt.xlabel('Variance')
plt.ylabel('Frequency')
plt.title('Distribution of Feature Variances')
plt.legend()
plt.show()

"""Problem 3: Influence of Hyper-parameters"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


# Define different perplexity values to explore
perplexity_values = [10, 100, 200]

# Create subplots for each perplexity value
plt.figure(figsize=(15, 5))
for i, perplexity in enumerate(perplexity_values):
    # Initialize T-SNE with the current perplexity
    tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42)
    x_tsne = tsne.fit_transform(processed_data_2)

    # Create a scatter plot for T-SNE visualization
    plt.subplot(1, len(perplexity_values), i + 1)
    plt.scatter(x_tsne[:, 0], x_tsne[:, 1], s=10)
    plt.title(f'T-SNE with Perplexity={perplexity}')
    plt.xlabel('Dimension 1 (T-SNE)')
    plt.ylabel('Dimension 2 (T-SNE)')

plt.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


# Define different learning rates to explore
learning_rates = [10, 100, 200]

# Create subplots for each learning rate
plt.figure(figsize=(15, 5))
for i, learning_rate in enumerate(learning_rates):
    # Initialize T-SNE with the current learning rate
    tsne = TSNE(n_components=2, learning_rate=learning_rate, random_state=42)
    x_tsne = tsne.fit_transform(processed_data_2)

    # Create a scatter plot for T-SNE visualization
    plt.subplot(1, len(learning_rates), i + 1)
    plt.scatter(x_tsne[:, 0], x_tsne[:, 1], s=10)
    plt.title(f'T-SNE with Learning Rate={learning_rate}')
    plt.xlabel('Dimension 1 (T-SNE)')
    plt.ylabel('Dimension 2 (T-SNE)')

plt.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split



# Define hyper-parameter values
clustering_criteria = ['single', 'ward']
perplexity_values = [10, 30, 50]
num_clusters_values = [3, 5, 7]

# Split the dataset into training and validation sets
X_train, X_valid = train_test_split(processed_data_2, test_size=0.2, random_state=42)

# Initialize dictionaries to store results
results = {}

# Iterate over hyper-parameter combinations
for criterion in clustering_criteria:
    for perplexity in perplexity_values:
        for num_clusters in num_clusters_values:
            # Perform hierarchical clustering
            clustering = AgglomerativeClustering(n_clusters=num_clusters, linkage=criterion)
            cluster_labels = clustering.fit_predict(X_train)

            # Evaluate clustering quality using silhouette score
            silhouette_avg = silhouette_score(X_train, cluster_labels)

            # Apply T-SNE dimensionality reduction
            tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42)
            x_tsne = tsne.fit_transform(X_train)

            # Store results for analysis
            results[(criterion, perplexity, num_clusters)] = {
                'Silhouette Score': silhouette_avg,
                'T-SNE Embedding': x_tsne,
                'Cluster Labels': cluster_labels
            }

# Analyze results (e.g., visualize clusters and feature selection)
for key, value in results.items():
    criterion, perplexity, num_clusters = key
    silhouette_score_value = value['Silhouette Score']
    x_tsne = value['T-SNE Embedding']
    cluster_labels = value['Cluster Labels']

    # Visualize T-SNE with cluster colors
    plt.figure(figsize=(8, 6))
    for cluster_id in range(num_clusters):
        plt.scatter(x_tsne[cluster_labels == cluster_id, 0], x_tsne[cluster_labels == cluster_id, 1],
                    label=f'Cluster {cluster_id + 1}', alpha=0.5)
    plt.title(f'T-SNE Visualization (Criterion: {criterion}, Perplexity: {perplexity}, Clusters: {num_clusters})')
    plt.xlabel('Dimension 1 (T-SNE)')
    plt.ylabel('Dimension 2 (T-SNE)')
    plt.legend()

    # Apply feature selection (e.g., logistic regression) based on cluster labels
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, cluster_labels)  # You may need to adjust this based on your feature selection approach

    # Evaluate feature selection quality (e.g., accuracy) on the validation set
    accuracy = clf.score(X_valid, clustering.predict(X_valid))

    print(f"Hyper-parameters: Criterion={criterion}, Perplexity={perplexity}, Clusters={num_clusters}")
    print(f"Silhouette Score: {silhouette_score_value}")
    print(f"Validation Accuracy: {accuracy}\n")

# Show plots if needed
plt.show()

from sklearn.datasets import make_classification
from sklearn.cluster import KMeans
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score



# Define a range of cluster numbers to evaluate
cluster_numbers = [9, 10, 11, 12, 13, 14, 15]

# Lists to store evaluation results
accuracy_scores = []
feature_selection_counts = []

for num_clusters in cluster_numbers:
    # Perform K-means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(X_evaluation_train)

    # Select the top K features based on ANOVA F-statistic
    k_best = SelectKBest(f_classif, k=num_clusters)  # Select features equal to the number of clusters
    X_new = k_best.fit_transform(X_evaluation_train, cluster_labels)

    # Train a classifier on the selected features
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_new, y_evaluation_train)

    # Test the classifier on the test set
    X_test_new = k_best.transform(X_evaluation_test)
    y_pred = clf.predict(X_test_new)

    # Evaluate accuracy
    accuracy = accuracy_score(y_evaluation_test, y_pred)
    accuracy_scores.append(accuracy)
    feature_selection_counts.append(num_clusters)

    print(f"Number of Clusters={num_clusters}, Accuracy={accuracy:.2f}")

# Plot the results
plt.figure(figsize=(8, 5))
plt.plot(feature_selection_counts, accuracy_scores, marker='o', linestyle='-')
plt.title("Accuracy vs. Number of Clusters for Feature Selection")
plt.xlabel("Number of Clusters")
plt.ylabel("Accuracy")
plt.grid(True)
plt.show()