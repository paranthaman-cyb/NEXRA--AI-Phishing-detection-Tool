import pandas as pd
import numpy as np
import os
import re
import joblib
from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
from sklearn.metrics import precision_recall_curve

# -------------------------
# Paths
# -------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data_path = os.path.join(BASE_DIR,"app","data","malicious_phish.csv")

model_path = os.path.join(BASE_DIR,"model","phishing_model.pkl")
columns_path = os.path.join(BASE_DIR,"model","feature_columns.pkl")
threshold_path = os.path.join(BASE_DIR,"model","threshold.pkl")

# -------------------------
# Load Dataset
# -------------------------

df = pd.read_csv(data_path)

print("Dataset loaded:",len(df))


# -------------------------
# Domain Extraction
# -------------------------

def extract_domain(url):

    if not isinstance(url,str) or url.strip()=="":
        return ""

    if not url.startswith(("http://","https://")):
        url = "http://"+url

    parsed = urlparse(url)

    domain = parsed.netloc

    if '@' in domain:
        domain = domain.split('@')[-1]

    return domain


# -------------------------
# Feature Engineering
# -------------------------

df['url_length'] = df['url'].apply(len)

df['dot_count'] = df['url'].apply(lambda x:x.count('.'))

df['subdomain_count'] = df['url'].apply(lambda x:max(0,x.count('.')-1))

df['has_at'] = df['url'].apply(lambda x:1 if '@' in x else 0)

df['has_https'] = df['url'].apply(lambda x:1 if 'https' in x else 0)

df['has_ip'] = df['url'].apply(lambda x:1 if re.search(r'\d+\.\d+\.\d+\.\d+',x) else 0)

df['hyphen_count'] = df['url'].apply(lambda x:x.count('-'))

df['digit_count'] = df['url'].apply(lambda x:sum(c.isdigit() for c in x))

df['has_query'] = df['url'].apply(lambda x:1 if '?' in x else 0)

df['has_path'] = df['url'].apply(
    lambda x:1 if '/' in x.replace("http://","").replace("https://","") else 0
)


# Suspicious words
suspicious_words = ['login','verify','secure','account','update','bank']

df['has_suspicious_word'] = df['url'].apply(
    lambda x:1 if any(word in str(x).lower() for word in suspicious_words) else 0
)


# Domain features
df['domain_length'] = df['url'].apply(lambda x:len(extract_domain(x)))

df['is_short_domain'] = df['domain_length'].apply(lambda x:1 if x<=12 else 0)


# -------------------------
# Labels
# -------------------------

df['label'] = df['type'].apply(lambda x:0 if x=="benign" else 1)


# -------------------------
# Feature Columns
# -------------------------

feature_columns = [

'url_length',
'dot_count',
'subdomain_count',
'has_at',
'has_https',
'has_ip',
'hyphen_count',
'digit_count',
'has_query',
'has_path',
'has_suspicious_word',
'domain_length',
'is_short_domain'

]

X = df[feature_columns]

y = df['label']


# -------------------------
# Train Test Split
# -------------------------

X_train,X_test,y_train,y_test = train_test_split(
X,y,test_size=0.2,random_state=42
)


# -------------------------
# Train Model
# -------------------------

model = RandomForestClassifier(
n_estimators=200,
max_depth=15,
class_weight="balanced",
random_state=42
)

model.fit(X_train,y_train)

print("Model trained")


# -------------------------
# Accuracy
# -------------------------

y_pred = model.predict(X_test)

print("Accuracy:",accuracy_score(y_test,y_pred))

print("\nConfusion Matrix")

print(confusion_matrix(y_test,y_pred))

print("\nClassification Report")

print(classification_report(y_test,y_pred))


# -------------------------
# Threshold Optimization
# -------------------------

y_scores = model.predict_proba(X_test)[:,1]

precision,recall,thresholds = precision_recall_curve(y_test,y_scores)

f1 = 2*(precision*recall)/(precision+recall+1e-10)

best_index = np.argmax(f1)

best_threshold = thresholds[min(best_index,len(thresholds)-1)]

print("Best threshold:",best_threshold)


# -------------------------
# Save Model
# -------------------------

joblib.dump(model,model_path)

joblib.dump(feature_columns,columns_path)

joblib.dump(best_threshold,threshold_path)

print("Model saved successfully")