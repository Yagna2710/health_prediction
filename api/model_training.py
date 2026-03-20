import os
import pickle
from data_preprocessing import generate_synthetic_data, DataPreprocessor
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def train_and_save_model():
    print("Generating synthetic dataset...")
    df = generate_synthetic_data(num_samples=10000)
    
    # Prepare features and target
    X = df.drop('RiskCategory', axis=1)
    y = df['RiskCategory']
    
    print("Preprocessing data...")
    preprocessor = DataPreprocessor()
    X_processed = preprocessor.fit_transform(X)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Training Random Forest with Grid Search CV...")
    # Setup Random Forest and Grid Search for hyperparameter tuning
    rf = RandomForestClassifier(random_state=42)
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
        'class_weight': ['balanced', None]
    }
    
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=cv, scoring='accuracy', n_jobs=-1, verbose=1)
    
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    print(f"Best params found: {grid_search.best_params_}")
    
    # Evaluation
    print("Evaluating model...")
    y_pred = best_model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Package model and preprocessor together
    pipeline = {
        'model': best_model,
        'preprocessor': preprocessor,
        'features': list(X.columns),
        'classes': best_model.classes_
    }
    
    model_path = os.path.join(os.path.dirname(__file__), 'health_rf_pipeline.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(pipeline, f)
        
    print(f"Successfully saved robust ML pipeline to {model_path}")

if __name__ == '__main__':
    train_and_save_model()
