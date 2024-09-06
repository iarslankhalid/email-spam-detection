from imblearn.over_sampling import SMOTE

def oversampling_data(X, y):
    """Apply SMOTE to oversample the minority class."""
    smote = SMOTE(sampling_strategy='minority')
    X_resampled, y_resampled = smote.fit_resample(X, y)
    return X_resampled, y_resampled
