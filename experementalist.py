import theorist

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def sample_condition(df, beta_samples):

    df_encoded = pd.get_dummies(df[['word', 'color', 'response_transition']], drop_first=True)
    # Dependent variable (correct/incorrect)

    # Independent variables (encoded)
    X_test = df_encoded.values

    # Step 4: Define the logistic function (sigmoid function)

    # Step 10: Make predictions on the test set using the sampled beta coefficients
    logits_samples_test = np.dot(beta_samples, X_test.T)
    predicted_probs_test = sigmoid(logits_samples_test)

    # Step 11: Calculate the mean and credible interval for the test predictions
    mean_predicted_prob_test = np.mean(predicted_probs_test, axis=0)
    lower_bound_test = np.percentile(predicted_probs_test, 2.5, axis=0)
    upper_bound_test = np.percentile(predicted_probs_test, 97.5, axis=0)

    uncertinity = upper_bound_test - lower_bound_test
    print(f"uncertinity: {uncertinity}")
    max_uncertinity = np.argmax(uncertinity)

    return max_uncertinity

