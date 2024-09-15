import theorist

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


def sigmoid(z):
    """
    Compute the sigmoid function for the input z.

    Parameters:
    z (array-like): Input array or scalar.

    Returns:
    array-like: Sigmoid of the input.
    """
    return 1 / (1 + np.exp(-z))

def sample_condition(df, beta_samples):
    """
    Sample the condition with the maximum uncertainty from the given DataFrame.

    Parameters:
    df (DataFrame): DataFrame containing the experimental data.
    beta_samples (array-like): Array of sampled beta coefficients from the Bayesian model.

    Returns:
    int: Index of the condition with the maximum uncertainty.
    """

    # Encode categorical variables
    df_encoded = pd.get_dummies(df[['word', 'color', 'response_transition']], drop_first=True)
    # Dependent variable (correct/incorrect)

    # Independent variables (encoded), Prepare test data
    X_test = df_encoded.values

    # Compute logits for the test set using the sampled beta coefficients
    logits_samples_test = np.dot(beta_samples, X_test.T)
    # Compute predicted probabilities using the sigmoid function
    predicted_probs_test = sigmoid(logits_samples_test)

    # Calculate the mean and credible interval for the test predictions
    mean_predicted_prob_test = np.mean(predicted_probs_test, axis=0)
    lower_bound_test = np.percentile(predicted_probs_test, 2.5, axis=0)
    upper_bound_test = np.percentile(predicted_probs_test, 97.5, axis=0)

    # Calculate uncertainty as the difference between upper and lower bounds
    uncertinity = upper_bound_test - lower_bound_test
    print(f"uncertinity: {uncertinity}")
    # Finde the index of the condition with the maximum uncertainty
    max_uncertinity = np.argmax(uncertinity)

    return max_uncertinity

