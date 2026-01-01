import streamlit as st
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Iris Classifier",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .big-font {
        font-size: 50px !important;
        font-weight: bold;
        color: #667eea;
        text-align: center;
    }
    .medium-font {
        font-size: 24px !important;
        font-weight: 600;
        color: #764ba2;
    }
    .highlight-box {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 10px 0;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #667eea;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px;
        border-radius: 8px;
        font-size: 16px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df["species"] = iris.target
    df["species_name"] = df["species"].map({0: "Setosa", 1: "Versicolor", 2: "Virginica"})
    return df, iris

df, iris = load_data()

# Header section
st.markdown('<p class="big-font">🌸 Iris Flower Classifier</p>', unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 20px; background: white; border-radius: 10px; margin-bottom: 20px;'>
        <p style='font-size: 18px; color: #555;'>
            Train a <strong>Random Forest</strong> model on the famous Iris dataset and make predictions with an elegant interface.
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.image("https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/doc/logos/scikit-learn-logo.png", width=200)
    st.markdown("## ⚙️ Model Configuration")
    
    st.markdown("### 🎛️ Hyperparameters")
    n_estimators = st.slider("🌲 Number of Trees", 10, 500, 100, help="Number of trees in the forest")
    max_depth = st.slider("📏 Max Depth", 0, 50, 5, help="Maximum depth of trees (0 = unlimited)")
    
    st.markdown("### 📊 Data Split")
    test_size_pct = st.slider("Test Set Size (%)", 10, 50, 30)
    random_state = st.number_input("🎲 Random State", value=42, step=1, help="Seed for reproducibility")
    
    st.markdown("---")
    st.markdown("### 📚 About")
    st.info("""
        The **Iris dataset** contains 150 samples of iris flowers with 4 features:
        - Sepal Length
        - Sepal Width  
        - Petal Length
        - Petal Width
        
        **Goal**: Classify into 3 species
    """)

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dataset Explorer", "🤖 Model Training", "🔮 Predictions", "📈 Visualizations"])

with tab1:
    st.markdown("## 🔍 Explore the Dataset")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📦 Total Samples", len(df))
    with col2:
        st.metric("📋 Features", len(df.columns) - 2)
    with col3:
        st.metric("🏷️ Classes", df["species"].nunique())
    with col4:
        st.metric("⚖️ Balance", "Perfect" if df["species"].value_counts().std() == 0 else "Good")
    
    st.markdown("### 📁 Raw Data")
    if st.checkbox("Show complete dataset", value=True):
        st.dataframe(df.style.highlight_max(axis=0, color='lightgreen').highlight_min(axis=0, color='lightcoral'), use_container_width=True)
    
    st.markdown("### 📊 Species Distribution")
    species_counts = df["species_name"].value_counts()
    fig_dist = px.pie(values=species_counts.values, names=species_counts.index, 
                      title="Distribution of Iris Species",
                      color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_dist, use_container_width=True)

with tab2:
    st.markdown("## 🤖 Train & Evaluate Model")
    
    # Prepare data
    X = df.iloc[:, :-2]
    y = df["species"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=(test_size_pct / 100.0), 
        random_state=int(random_state), stratify=y
    )
    
    # Train model
    with st.spinner("🔄 Training Random Forest model..."):
        model = RandomForestClassifier(
            n_estimators=int(n_estimators), 
            max_depth=(None if int(max_depth) == 0 else int(max_depth)), 
            random_state=int(random_state)
        )
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
    
    st.success("✅ Model trained successfully!")
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🎯 Test Accuracy", f"{acc:.2%}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🏋️ Training Samples", len(X_train))
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🧪 Test Samples", len(X_test))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Confusion Matrix
    st.markdown("### 🔢 Confusion Matrix")
    cm = confusion_matrix(y_test, y_pred)
    fig_cm = px.imshow(cm, 
                       labels=dict(x="Predicted", y="Actual", color="Count"),
                       x=iris.target_names, y=iris.target_names,
                       color_continuous_scale='Blues',
                       text_auto=True)
    fig_cm.update_layout(title="Model Performance Matrix")
    st.plotly_chart(fig_cm, use_container_width=True)
    
    # Feature Importance
    st.markdown("### 🌟 Feature Importance")
    feat_imp = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    fig_imp = px.bar(feat_imp, x='Importance', y='Feature', 
                     orientation='h',
                     color='Importance',
                     color_continuous_scale='Viridis',
                     title="Which features matter most?")
    st.plotly_chart(fig_imp, use_container_width=True)

with tab3:
    st.markdown("## 🔮 Make Predictions")
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
            <p style='color: white; text-align: center; font-size: 16px; margin: 0;'>
                🌺 Enter flower measurements to predict the species
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    defaults = X.mean()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌿 Sepal Measurements")
        sepal_length = st.number_input(
            "📏 Sepal Length (cm)", 
            float(X["sepal length (cm)"].min()), 
            float(X["sepal length (cm)"].max()), 
            float(defaults["sepal length (cm)"]),
            step=0.1
        )
        sepal_width = st.number_input(
            "📐 Sepal Width (cm)", 
            float(X["sepal width (cm)"].min()), 
            float(X["sepal width (cm)"].max()), 
            float(defaults["sepal width (cm)"]),
            step=0.1
        )
    
    with col2:
        st.markdown("### 🌸 Petal Measurements")
        petal_length = st.number_input(
            "📏 Petal Length (cm)", 
            float(X["petal length (cm)"].min()), 
            float(X["petal length (cm)"].max()), 
            float(defaults["petal length (cm)"]),
            step=0.1
        )
        petal_width = st.number_input(
            "📐 Petal Width (cm)", 
            float(X["petal width (cm)"].min()), 
            float(X["petal width (cm)"].max()), 
            float(defaults["petal width (cm)"]),
            step=0.1
        )
    
    if st.button("🔮 Predict Species"):
        sample = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        pred = model.predict(sample)[0]
        proba = model.predict_proba(sample)
        max_proba = proba.max()
        
        # Display prediction
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                        padding: 30px; border-radius: 15px; text-align: center; margin-top: 20px;'>
                <h2 style='color: white; margin: 0;'>🌺 Predicted Species</h2>
                <h1 style='color: white; font-size: 48px; margin: 10px 0;'>{iris.target_names[pred].upper()}</h1>
                <p style='color: white; font-size: 20px; margin: 0;'>Confidence: {max_proba:.1%}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Probability distribution
        st.markdown("### 📊 Probability Distribution")
        prob_df = pd.DataFrame({
            'Species': iris.target_names,
            'Probability': proba[0]
        })
        fig_prob = px.bar(prob_df, x='Species', y='Probability',
                         color='Probability',
                         color_continuous_scale='RdYlGn',
                         title="Confidence for each species")
        fig_prob.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig_prob, use_container_width=True)

with tab4:
    st.markdown("## 📈 Advanced Visualizations")
    
    # Feature relationships
    st.markdown("### 🔗 Feature Relationships")
    viz_type = st.selectbox("Select visualization", 
                           ["Pairwise Scatter", "3D Scatter", "Box Plots"])
    
    if viz_type == "Pairwise Scatter":
        feature_x = st.selectbox("X-axis feature", X.columns, index=0)
        feature_y = st.selectbox("Y-axis feature", X.columns, index=1)
        
        fig_scatter = px.scatter(df, x=feature_x, y=feature_y, 
                                color='species_name',
                                title=f"{feature_x} vs {feature_y}",
                                color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    elif viz_type == "3D Scatter":
        fig_3d = px.scatter_3d(df, 
                              x='sepal length (cm)', 
                              y='sepal width (cm)', 
                              z='petal length (cm)',
                              color='species_name',
                              title="3D Feature Space",
                              color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig_3d, use_container_width=True)
    
    else:  # Box Plots
        selected_feature = st.selectbox("Select feature", X.columns)
        fig_box = px.box(df, x='species_name', y=selected_feature,
                        color='species_name',
                        title=f"Distribution of {selected_feature} by Species",
                        color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_box, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 20px; background: white; border-radius: 10px;'>
        <p style='color: #666; margin: 0;'>
            🚀 Built with Streamlit | 🌸 Iris Dataset from scikit-learn | 💜 Machine Learning Demo
        </p>
        <p style='color: #888; font-size: 12px; margin-top: 10px;'>
            Run with: <code>streamlit run classification.py</code>
        </p>
    </div>
""", unsafe_allow_html=True)