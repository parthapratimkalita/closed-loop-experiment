import time

import numpy as np
import pandas as pd

import experiment_runner
import experimentalist
import read_experiment_data
import theorist

for i in range(5):
    if i == 0:
        timelines = experiment_runner.sample_trials("initial")
        experiment_runner.run_experiment(timelines[0])
        timeline0 = pd.DataFrame.from_dict(timelines[0])

        print(timeline0)
        time.sleep(50)
        filtered_df = read_experiment_data.read_experiment_data()
        timeline0['rt'] = filtered_df['rt']
        timeline0['response'] = filtered_df['response']

        df_encoded = pd.get_dummies(timeline0[['word', 'color', 'response_transition']], drop_first=True)

        X_train = df_encoded.values
        y_train = timeline0['rt'].values

        # Step 8: Run MCMC sampling for Bayesian linear regression
        n_samples_mcmc = 5000  # Number of MCMC samples
        step_size = 0.1  # Step size for proposals
        beta_samples_train, sigma2_samples_train = theorist.run_theory(iteration="initial", posterior_means=0,
                                                                       posterior_variances=0,
                                                                       n_samples_mcmc=n_samples_mcmc,
                                                                       step_size=step_size, X_train=X_train,
                                                                       y_train=y_train)
    elif i < 2:
        timelines = experiment_runner.sample_trials("initial")
        experiment_runner.run_experiment(timelines[0])
        timeline0 = pd.DataFrame.from_dict(timelines[0])

        time.sleep(50)
        filtered_df = read_experiment_data.read_experiment_data()
        timeline0['rt'] = filtered_df['rt']
        timeline0['response'] = filtered_df['response']

        df_encoded = pd.get_dummies(timeline0[['word', 'color', 'response_transition']], drop_first=True)

        X_train = df_encoded.values
        y_train = timeline0['rt'].values

        posterior_means = np.mean(beta_samples_train, axis=0)
        posterior_variances = np.var(beta_samples_train, axis=0)
        beta_samples_train, sigma2_samples_train = theorist.run_theory(iteration="update",
                                                                       posterior_means=posterior_means,
                                                                       posterior_variances=posterior_variances,
                                                                       n_samples_mcmc=n_samples_mcmc,
                                                                       step_size=step_size, X_train=X_train,
                                                                       y_train=y_train)
    else:
        timelines = experiment_runner.sample_trials("initial")
        timeline0 = pd.DataFrame.from_dict(timelines[0])

        maximum_uncertinity = experimentalist.sample_condition(timeline0, beta_samples_train)
        timeline0_as_a_dictionary = timeline0.iloc[maximum_uncertinity].to_dict()
        print(timeline0_as_a_dictionary)

        timelines = experiment_runner.sample_trials("update")

        frequency = []
        for i in range(len(timelines)):
            p = 0
            timeline = timelines[i]
            for j in range(len(timeline)):

                if timeline[j]["word"] == timeline0_as_a_dictionary["word"] and timeline[j]["color"] == \
                    timeline0_as_a_dictionary["color"] and timeline[j]["response_transition"] == \
                    timeline0_as_a_dictionary["response_transition"]:
                    p = p + 1
            frequency.append(p)

        max_frequency = np.argmax(frequency)

        timeline0 = pd.DataFrame.from_dict(timelines[max_frequency])
        experiment_runner.run_experiment(timelines[max_frequency])

        time.sleep(50)
        filtered_df = read_experiment_data.read_experiment_data()
        timeline0['rt'] = filtered_df['rt']
        timeline0['response'] = filtered_df['response']

        df_encoded = pd.get_dummies(timeline0[['word', 'color', 'response_transition']], drop_first=True)

        X_train = df_encoded.values
        y_train = timeline0['rt'].values

        posterior_means = np.mean(beta_samples_train, axis=0)
        posterior_variances = np.var(beta_samples_train, axis=0)
        beta_samples_train, sigma2_samples_train = theorist.run_theory(iteration="update",
                                                                       posterior_means=posterior_means,
                                                                       posterior_variances=posterior_variances,
                                                                       n_samples_mcmc=n_samples_mcmc,
                                                                       step_size=step_size, X_train=X_train,
                                                                       y_train=y_train)
