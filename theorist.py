import pandas as pd
import json
import re
import os
import numpy as np

def run_theory(iteration, posterior_means, posterior_variances, n_samples_mcmc, step_size, X_train, y_train):
    print('Theorist')


    # Step 4: Define the likelihood for Bayesian linear regression
    def gaussian_likelihood(X, y, beta, sigma2):
        residuals = y - np.dot(X, beta)
        return -0.5 * np.sum(np.log(2 * np.pi * sigma2) + (residuals ** 2) / sigma2)

    if iteration == "initial":


        # Step 5: Define a normal prior for beta coefficients and inverse-gamma prior for sigma2
        def log_prior(beta, sigma2):
            beta_prior = -0.5 * np.sum(beta ** 2 / 100)  # Normal prior for beta
            sigma2_prior = -1.0 * np.log(sigma2)  # Weak prior for variance
            return beta_prior + sigma2_prior

        # Step 6: Define the log-posterior combining likelihood and prior
        def log_posterior(X, y, beta, sigma2):
            return log_prior(beta, sigma2) + gaussian_likelihood(X, y, beta, sigma2)

        # Step 7: MCMC sampling using Metropolis-Hastings algorithm
        def metropolis_hastings_regression(X, y, n_samples, step_size):
            n_params = X.shape[1]  # Number of features (parameters)
            beta_current = np.random.randn(n_params)  # Initial guess for beta
            sigma2_current = 1.0  # Initial guess for variance
            log_posterior_current = log_posterior(X, y, beta_current, sigma2_current)
            
            beta_samples = np.zeros((n_samples, n_params))  # Store beta samples
            sigma2_samples = np.zeros(n_samples)  # Store sigma^2 samples
            acceptance_count = 0
            
            for i in range(n_samples):
                # Propose new parameters for beta and sigma2
                beta_proposal = beta_current + np.random.randn(n_params) * step_size
                sigma2_proposal = np.abs(sigma2_current + np.random.randn() * step_size)
                
                # Compute the log-posterior for the proposed parameters
                log_posterior_proposal = log_posterior(X, y, beta_proposal, sigma2_proposal)
                
                # Acceptance criterion (log-acceptance ratio)
                log_accept_ratio = log_posterior_proposal - log_posterior_current
                accept = np.log(np.random.rand()) < log_accept_ratio
                
                if accept:
                    beta_current = beta_proposal
                    sigma2_current = sigma2_proposal
                    log_posterior_current = log_posterior_proposal
                    acceptance_count += 1
                
                # Store the current samples
                beta_samples[i, :] = beta_current
                sigma2_samples[i] = sigma2_current
            
            acceptance_rate = acceptance_count / n_samples
            print(f"Acceptance rate: {acceptance_rate:.3f}")
            
            return beta_samples, sigma2_samples
        
        return metropolis_hastings_regression(X_train, y_train, n_samples_mcmc, step_size)
    

        # Step 8: Run MCMC sampling for Bayesian linear regression
        n_samples_mcmc = 5000  # Number of MCMC samples
        step_size = 0.1        # Step size for proposals
        beta_samples_train, sigma2_samples_train = metropolis_hastings_regression(X_train, y_train, n_samples_mcmc, step_size)

        # Step 9: Make predictions on the test set using the posterior samples
        logits_samples_test = np.dot(beta_samples_train, X_test.T)
        predicted_reaction_times_test = logits_samples_test  # No sigmoid, since it's linear regression

        # Step 10: Calculate the mean and credible interval for the test predictions
        mean_predicted_reaction_time_test = np.mean(predicted_reaction_times_test, axis=0)
        lower_bound_test = np.percentile(predicted_reaction_times_test, 2.5, axis=0)
        upper_bound_test = np.percentile(predicted_reaction_times_test, 97.5, axis=0)

        # Print results
        print("Mean Predicted Reaction Times:", mean_predicted_reaction_time_test[:10])
        print("Credible Interval Lower Bound:", lower_bound_test[:10])
        print("Credible Interval Upper Bound:", upper_bound_test[:10])

    else:

        # Step 5: Define the new prior using the posterior from the previous step
        def log_prior_from_posterior(beta):
            # Define the prior using the posterior mean and variance
            return -0.5 * np.sum((beta - posterior_means) ** 2 / posterior_variances)

        # Step 6: Redefine the log-posterior to use the new prior
        def log_posterior_with_new_prior(X, y, beta, sigma2):
            return log_prior_from_posterior(beta) + gaussian_likelihood(X, y, beta, sigma2)

        # Step 7: MCMC sampling using the new prior based on the previous posterior
        def metropolis_hastings_with_new_prior(X, y, n_samples, step_size):
            n_params = X.shape[1]  # Number of features (parameters)
            beta_current = np.random.randn(n_params)  # Initial guess for beta
            sigma2_current = 1.0  # Initial guess for variance
            log_posterior_current = log_posterior_with_new_prior(X, y, beta_current, sigma2_current)
            
            beta_samples = np.zeros((n_samples, n_params))  # Store beta samples
            sigma2_samples = np.zeros(n_samples)  # Store sigma^2 samples
            acceptance_count = 0
            
            for i in range(n_samples):
                # Propose new parameters for beta and sigma2
                beta_proposal = beta_current + np.random.randn(n_params) * step_size
                sigma2_proposal = np.abs(sigma2_current + np.random.randn() * step_size)
                
                # Compute the log-posterior for the proposed parameters
                log_posterior_proposal = log_posterior_with_new_prior(X, y, beta_proposal, sigma2_proposal)
                
                # Acceptance criterion (log-acceptance ratio)
                log_accept_ratio = log_posterior_proposal - log_posterior_current
                accept = np.log(np.random.rand()) < log_accept_ratio
                
                if accept:
                    beta_current = beta_proposal
                    sigma2_current = sigma2_proposal
                    log_posterior_current = log_posterior_proposal
                    acceptance_count += 1
                
                # Store the current samples
                beta_samples[i, :] = beta_current
                sigma2_samples[i] = sigma2_current
            
            acceptance_rate = acceptance_count / n_samples
            print(f"Acceptance rate: {acceptance_rate:.3f}")
            
            return beta_samples, sigma2_samples

        
        return metropolis_hastings_with_new_prior(X_train, y_train, n_samples_mcmc, step_size)

        # Step 1: Identify the most uncertain points based on the credible interval width
        uncertain_points_threshold = 0.15  # Define a threshold for high uncertainty
        uncertain_points_idx = np.where(credible_interval_width_test >= uncertain_points_threshold)[0]

        # Select these uncertain points from the test set
        X_uncertain = X_test[uncertain_points_idx]
        y_uncertain = y_test[uncertain_points_idx]

        # Step 2: Add the uncertain points back into the training set
        X_train_augmented = np.vstack([X_train, X_uncertain])
        y_train_augmented = np.hstack([y_train, y_uncertain])

        # Step 5: Run the MCMC with the new prior based on the previous posterior
        beta_samples_train_augmented_with_posterior_prior = metropolis_hastings_with_new_prior(X_train_augmented, y_train_augmented, n_samples_mcmc, step_size)

        # Step 6: Continue with the predictions on the test set...

        # Step 10: Make predictions on the test set using the sampled beta coefficients
        logits_samples_test = np.dot(beta_samples_train_augmented_with_posterior_prior, X_test.T)  # This is the correct dot product
        predicted_probs_test = sigmoid(logits_samples_test)

        # Step 11: Calculate the mean and credible interval for the test predictions
        mean_predicted_prob_test = np.mean(predicted_probs_test, axis=0)
        lower_bound_test = np.percentile(predicted_probs_test, 2.5, axis=0)
        upper_bound_test = np.percentile(predicted_probs_test, 97.5, axis=0)
        print(upper_bound_test[:10] - lower_bound_test[:10])
