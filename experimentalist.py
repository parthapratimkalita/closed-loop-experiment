import numpy as np
import pandas as pd


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def sample_condition(df, beta_samples):
    df_encoded = pd.get_dummies(df[['word', 'color', 'response_transition']], drop_first=True)

    X_test = df_encoded.values

    logits_samples_test = np.dot(beta_samples, X_test.T)
    predicted_probs_test = sigmoid(logits_samples_test)

    mean_predicted_prob_test = np.mean(predicted_probs_test, axis=0)
    lower_bound_test = np.percentile(predicted_probs_test, 2.5, axis=0)
    upper_bound_test = np.percentile(predicted_probs_test, 97.5, axis=0)

    uncertainty = upper_bound_test - lower_bound_test
    print(f"uncertainty: {uncertainty}")
    max_uncertainty = np.argmax(uncertainty)

    return max_uncertainty
