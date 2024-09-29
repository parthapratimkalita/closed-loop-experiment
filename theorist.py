import numpy as np


def run_theory(iteration, posterior_means, posterior_variances, n_samples_mcmc, step_size, X_train, y_train):
    def gaussian_likelihood(X, y, beta, sigma2):
        residuals = y - np.dot(X, beta)
        return -0.5 * np.sum(np.log(2 * np.pi * sigma2) + (residuals ** 2) / sigma2)

    def log_prior(beta, sigma2):
        beta_prior = -0.5 * np.sum(beta ** 2 / 100)
        sigma2_prior = -1.0 * np.log(sigma2)
        return beta_prior + sigma2_prior

    def log_posterior(X, y, beta, sigma2):
        return log_prior(beta, sigma2) + gaussian_likelihood(X, y, beta, sigma2)

    def metropolis_hastings_regression(X, y, n_samples, step_size):
        n_params = X.shape[1]
        beta_current = np.random.randn(n_params)
        sigma2_current = 1.0
        log_posterior_current = log_posterior(X, y, beta_current, sigma2_current)

        beta_samples = np.zeros((n_samples, n_params))
        sigma2_samples = np.zeros(n_samples)
        acceptance_count = 0

        for i in range(n_samples):
            beta_proposal = beta_current + np.random.randn(n_params) * step_size
            sigma2_proposal = np.abs(sigma2_current + np.random.randn() * step_size)
            log_posterior_proposal = log_posterior(X, y, beta_proposal, sigma2_proposal)
            log_accept_ratio = log_posterior_proposal - log_posterior_current
            accept = np.log(np.random.rand()) < log_accept_ratio

            if accept:
                beta_current = beta_proposal
                sigma2_current = sigma2_proposal
                log_posterior_current = log_posterior_proposal
                acceptance_count += 1

            beta_samples[i, :] = beta_current
            sigma2_samples[i] = sigma2_current

        print(f'Acceptance rate: {acceptance_count / n_samples:.3f}')
        return beta_samples, sigma2_samples

    if iteration == 'initial':
        return metropolis_hastings_regression(X_train, y_train, n_samples_mcmc, step_size)
    else:
        def log_prior_from_posterior(beta):
            return -0.5 * np.sum((beta - posterior_means) ** 2 / posterior_variances)

        def log_posterior_with_new_prior(X, y, beta, sigma2):
            return log_prior_from_posterior(beta) + gaussian_likelihood(X, y, beta, sigma2)

        def metropolis_hastings_with_new_prior(X, y, n_samples, step_size):
            n_params = X.shape[1]
            beta_current = np.random.randn(n_params)
            sigma2_current = 1.0
            log_posterior_current = log_posterior_with_new_prior(X, y, beta_current, sigma2_current)

            beta_samples = np.zeros((n_samples, n_params))
            sigma2_samples = np.zeros(n_samples)
            acceptance_count = 0

            for i in range(n_samples):
                beta_proposal = beta_current + np.random.randn(n_params) * step_size
                sigma2_proposal = np.abs(sigma2_current + np.random.randn() * step_size)
                log_posterior_proposal = log_posterior_with_new_prior(X, y, beta_proposal, sigma2_proposal)
                log_accept_ratio = log_posterior_proposal - log_posterior_current
                accept = np.log(np.random.rand()) < log_accept_ratio

                if accept:
                    beta_current = beta_proposal
                    sigma2_current = sigma2_proposal
                    log_posterior_current = log_posterior_proposal
                    acceptance_count += 1

                beta_samples[i, :] = beta_current
                sigma2_samples[i] = sigma2_current

            print(f'Acceptance rate: {acceptance_count / n_samples:.3f}')
            return beta_samples, sigma2_samples

        return metropolis_hastings_with_new_prior(X_train, y_train, n_samples_mcmc, step_size)
