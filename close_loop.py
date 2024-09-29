import time
import numpy as np
import pandas as pd
from pandas import DataFrame

import experiment_runner
import experimentalist
import read_experiment_data
import theorist


def run_iteration(i, beta_samples_train, n_samples_mcmc, step_size):
    timelines = experiment_runner.sample_trials('initial')
    experiment_runner.run_experiment(timelines[0])

    timeline0 = DataFrame.from_dict(timelines[0])
    time.sleep(50)
    filtered_df = read_experiment_data.read_experiment_data()
    timeline0['rt'] = filtered_df['rt']
    timeline0['response'] = filtered_df['response']
    df_encoded = pd.get_dummies(timeline0[['word', 'color', 'response_transition']], drop_first=True)
    X_train = df_encoded.values
    y_train = timeline0['rt'].values

    if i == 0:
        return theorist.run_theory('initial', 0, 0, n_samples_mcmc, step_size, X_train, y_train)
    else:
        posterior_means = np.mean(beta_samples_train, axis=0)
        posterior_variances = np.var(beta_samples_train, axis=0)
        return theorist.run_theory('update', posterior_means, posterior_variances, n_samples_mcmc, step_size, X_train,
                                   y_train)


def run_experiment_with_max_uncertainty(beta_samples_train, n_samples_mcmc, step_size):
    timelines = experiment_runner.sample_trials('initial')
    timeline0 = DataFrame.from_dict(timelines[0])
    max_uncertainty = experimentalist.sample_condition(timeline0, beta_samples_train)
    timeline0_dict = timeline0.iloc[max_uncertainty].to_dict()
    timelines = experiment_runner.sample_trials('update')
    max_freq_timeline = max(timelines, key=lambda t: sum(1 for trial in t if
                                                         trial['word'] == timeline0_dict['word'] and trial['color'] ==
                                                         timeline0_dict['color'] and trial['response_transition'] ==
                                                         timeline0_dict['response_transition']))
    experiment_runner.run_experiment(max_freq_timeline)

    time.sleep(50)
    filtered_df = read_experiment_data.read_experiment_data()
    timeline0 = DataFrame.from_dict(max_freq_timeline)
    timeline0['rt'] = filtered_df['rt']
    timeline0['response'] = filtered_df['response']
    df_encoded = pd.get_dummies(timeline0[['word', 'color', 'response_transition']], drop_first=True)
    X_train = df_encoded.values
    y_train = timeline0['rt'].values
    posterior_means = np.mean(beta_samples_train, axis=0)
    posterior_variances = np.var(beta_samples_train, axis=0)
    return theorist.run_theory('update', posterior_means, posterior_variances, n_samples_mcmc, step_size, X_train,
                               y_train)


if __name__ == '__main__':
    n_samples_mcmc = 5000
    step_size = 0.1
    beta_samples_train, sigma2_samples_train = None, None

    for i in range(5):
        if i < 2:
            beta_samples_train, sigma2_samples_train = run_iteration(i, beta_samples_train, n_samples_mcmc, step_size)
        else:
            beta_samples_train, sigma2_samples_train = run_experiment_with_max_uncertainty(beta_samples_train,
                                                                                           n_samples_mcmc, step_size)
