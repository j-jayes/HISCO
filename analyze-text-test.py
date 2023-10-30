import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Download stopwords if you haven't already
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize lemmatizer and stopwords list
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Define a preprocessing function
def preprocess(text):
    words = nltk.word_tokenize(text)
    words = [lemmatizer.lemmatize(word) for word in words if word.isalnum() and word not in stop_words]
    return ' '.join(words)

# read in data from "data/occupations/3-digit-occupations.csv"
df = pd.read_csv('data/occupations/3-digit-occupations.csv')
df['first_digit'] = df['Number'].apply(lambda x: int(str(x)[0]))


# Apply the preprocessing function to the DataFrame
df['processed_description'] = df['Description (tasks and duties)'].apply(preprocess)

# Convert to TF-IDF
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(df['processed_description'])

from sklearn.decomposition import PCA

# Choose the number of components, for visualization, we'll use 2
n_components = 2
pca = PCA(n_components=n_components)

# Apply PCA
X_pca = pca.fit_transform(X.toarray())

import matplotlib.pyplot as plt
import numpy as np

def plot_embedding_color(X, labels, title):
    unique_labels = np.unique(labels)
    colors = plt.cm.jet(np.linspace(0, 1, len(unique_labels)))
    
    for i, label in enumerate(unique_labels):
        idx = labels == label
        plt.scatter(X[idx, 0], X[idx, 1], color=colors[i], alpha=0.6, edgecolors='w', linewidth=0.5, label=f"Code {label}XX")
    
    plt.title(title)
    plt.xlabel(f"Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.2f}%)")
    plt.ylabel(f"Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.2f}%)")
    plt.legend()
    plt.grid(True)
    plt.show()

# Visualize PCA results colored by the first digit of the occupational code
plot_embedding_color(X_pca, df['first_digit'].values, "PCA Embedding of Occupations by Code")


import umap

# Fit UMAP model
reducer = umap.UMAP(random_state=42)
X_umap = reducer.fit_transform(X.toarray())

plot_embedding_color(X_umap, df['first_digit'].values, "UMAP Embedding of Occupations by Code")

import plotly.express as px

def interactive_umap_plot(X, labels, hover_data, title):
    # Create a DataFrame for the UMAP results
    umap_df = pd.DataFrame({
        'UMAP 1': X[:, 0],
        'UMAP 2': X[:, 1],
        'label': labels,
        **hover_data  # This unpacks the hover_data dictionary into columns
    })
    
    fig = px.scatter(
        umap_df,
        x='UMAP 1',
        y='UMAP 2',
        color='label',
        hover_data=list(hover_data.keys()),  # This specifies which columns to include in the hover tooltips
        title=title,
        color_discrete_sequence=px.colors.qualitative.Set1  # This uses a predefined color sequence
    )
    
    fig.show()

# Create a dictionary of additional hover data
hover_data = {
    'Code': df['Number'],
    'Description': df['Description (tasks and duties)'],
    'Name': df['Name']
}

interactive_umap_plot(X_umap, df['first_digit'].values, hover_data, "Interactive UMAP Embedding of Occupations by Code")
