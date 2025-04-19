import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# Columns from NSL-KDD dataset
columns = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins',
    'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root',
    'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds',
    'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate',
    'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
    'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count',
    'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
    'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
    'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
    'dst_host_srv_rerror_rate', 'label', 'difficulty_level'
]

def load_data(file_path):
    df = pd.read_csv(file_path, names=columns)
    return df

def preprocess_data(df):
    # Drop constant or non-relevant columns
    df = df.drop(['num_outbound_cmds'], axis=1)

    # Encode categorical features
    label_enc = LabelEncoder()
    for col in ['protocol_type', 'service', 'flag']:
        df[col] = label_enc.fit_transform(df[col])

    # Label: normal = 0, anomaly = 1
    df['label'] = df['label'].apply(lambda x: 0 if x == 'normal' else 1)

    # Split features and labels
    X = df.drop(['label', 'difficulty_level'], axis=1)
    y = df['label']

    # Normalize data
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y
