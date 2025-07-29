import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from typing import Tuple, List, Dict, Any

class DecisionTreePatternAgent:
    def __init__(self, max_depth: int = 4, random_state: int = 42):
        self.max_depth = max_depth
        self.random_state = random_state
        self.model = None
        self.feature_names = None
        self.target_name = None

    def preprocess(self, df: pd.DataFrame, target_col: str) -> Tuple[pd.DataFrame, pd.Series]:
        # Encode categorical variables and handle missing values simply
        df = df.copy()
        y = df[target_col]
        X = df.drop(columns=[target_col])
        # Simple encoding for demo: convert all object columns to category codes
        for col in X.select_dtypes(include=['object', 'category']).columns:
            X[col] = X[col].astype('category').cat.codes
        X = X.fillna(-1)
        return X, y

    def extract_patterns(self, df: pd.DataFrame, target_col: str) -> Dict[str, Any]:
        X, y = self.preprocess(df, target_col)
        self.feature_names = X.columns.tolist()
        self.target_name = target_col
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=self.random_state
        )
        self.model = DecisionTreeClassifier(max_depth=self.max_depth, random_state=self.random_state)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        # Extract rules as text
        tree_rules = export_text(self.model, feature_names=list(X.columns))
        # Extract top 3 rules (first 3 'if' blocks)
        rules = []
        for line in tree_rules.split('\n'):
            if line.strip().startswith('if'):
                rules.append(line.strip())
            if len(rules) >= 3:
                break
        return {
            'accuracy': accuracy,
            'rules': rules,
            'tree_text': tree_rules
        } 