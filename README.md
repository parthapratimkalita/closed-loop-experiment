# Group: Krishnendu Bose, Alexander Ditz, Partha Pratim Kalita, Hannes Voss

# This is our Closed-Loop-Experiment for the course Automated Scientific Discovery at the University of Osnabrück. We developed an experiment for modeling attentional mechanisms with a stroop task experiment.

## Setup and Installation

**1. Open a terminal and clone this repository:**

```bash
git clone https://github.com/parthapratimkalita/closed-loop-experiment.git
```

**2. Create a virtual environment (optional but recommended):**

We use conda to create the virtual environment. To install conda you can follow the
official [documentation](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

```bash
conda create -n closed-loop python=3.9 nb_conda_kernels
conda activate closed-loop
```

**3. Install the required dependencies:** <br>

```bash
pip install -r requirements.txt
```

## Running the project

If you want to start the experiment you have to run the closed_loop.py file.
Once you run the program the experiment data automatically gets downloaded in the Download folder of your local machine and the theorist tries to fit this data.


