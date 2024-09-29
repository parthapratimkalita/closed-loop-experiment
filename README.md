# Stroop Task Closed-Loop Experiment

This repository contains the code for a closed-loop experiment on the Stroop task. The experiment is designed to test
the effect of congruency on reaction times and accuracy in a Stroop task. The experiment uses a Bayesian adaptive design
to update the experiment based on the collected data.

## Project Structure

- `close_loop.py`: Main script to run the closed-loop experiment.
- `experiment_runner.py`: Module for sampling trials and running experiments.
- `experimentalist.py`: Module for sampling conditions with maximum uncertainty.
- `read_experiment_data.py`: Module for reading experiment data.
- `theorist.py`: Module for running theoretical models.
- `index.html`: HTML file for running the experiment in a web browser.
- `requirements.txt`: List of dependencies required for the project.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/hannesvoss/closed-loop-experiment.git
    cd closed-loop-experiment
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the `close_loop.py` file to start the closed-loop experiment:
    ```sh
    python close_loop.py
    ```

2. The experiment will run in a web browser, and data will be collected and processed automatically.

## Dependencies

- `numpy~=2.0.2`
- `pandas~=2.2.3`
- `sweetbean~=0.0.42`
- `sweetpea~=0.2.7`

## Project Workflow

1. **Sampling Trials**: The `experiment_runner.sample_trials` function samples initial trials for the experiment.
2. **Running Experiments**: The `experiment_runner.run_experiment` function runs the experiment using the sampled
   trials.
3. **Reading Data**: The `read_experiment_data.read_experiment_data` function reads the collected data.
4. **Running Theoretical Models**: The `theorist.run_theory` function runs theoretical models to update the experiment
   based on the collected data.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

This project uses the following libraries:

- [NumPy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [SweetBean](https://github.com/sweetbean-org/sweetbean)
- [SweetPea](https://github.com/sweetpea-org/sweetpea)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.