import os
import webbrowser

import pandas as pd
from sweetpea import (
    Factor, WithinTrial, Transition, AtMostKInARow,
    CrossBlock, synthesize_trials, CMSGen, RandomGen, experiments_to_dicts
)

"""
Stroop Task
******************************
factors (levels):
- current color (red, blue, green, yellow)
- current word (red, blue, green, yellow)
- congruency (congruent, incongruent): Factor dependent on color and word.
- correct response (up, down, left right): Factor dependent on color.
- response Transition (repetition, switch). Factor dependent on response:

design:
- counterbalancing color x word x response Transition
- no more than 7 response repetitions in a row
- no more than 7 response switches in a row
"""


# Define congruency factor
def congruent(color, word):
    return color == word


def incongruent(color, word):
    return not congruent(color, word)

# Define response factor
def response_r(color):
    return color == "red"

def response_g(color):
    return color == "green"

def response_b(color):
    return color == "blue"

def response_y(color):
    return color == "yellow"

# Define response transition factor
def response_repeat(response):
    return response[0] == response[-1]


def response_switch(response):
    return not response_repeat(response)

# Defining the predicate for the f-level of the "correct response" parameter
def is_correct_r(color):
    return color == 'red'

# Defining the predicate for the j-level of the "correct response" parameter
def is_correct_g(color):
    return color == 'green'

# Defining the predicate for the r-level of the "correct response" parameter
def is_correct_b(color):
    return color == 'blue'

# Defining the predicate for the z-level of the "correct response" parameter
def is_correct_y(color):
    return color == 'yellow'

# Positive feedback after correct responses (remember the correct data variable has boolean levels itself)
def is_positive_feedback(correct):
    return correct

# Negative feedback after incorrect responses
def is_negative_feedback(correct):
    return not correct


def sample_trials(iteration):
    from sweetpea import DerivedLevel

    # Define color and word factors

    color      = Factor("color",  ["red", "green", "blue", "yellow"])
    word       = Factor("word", ["red", "green", "blue", "yellow"])

    # Define congruency levels based on color and word
    conLevel = DerivedLevel("con", WithinTrial(congruent,   [color, word]))
    incLevel = DerivedLevel("inc", WithinTrial(incongruent,   [color, word]))
    congruency = Factor("congruency", [conLevel, incLevel])

    # Define response levels based on color
    response = Factor("correct_response", [
        DerivedLevel("r", WithinTrial(response_r,   [color])),
        DerivedLevel("g", WithinTrial(response_g,   [color])),
        DerivedLevel("b", WithinTrial(response_b, [color])),
        DerivedLevel("y", WithinTrial(response_y, [color])),
    ])

    # Define response transition levels based on response
    resp_transition = Factor("response_transition", [
        DerivedLevel("repeat", Transition(response_repeat, [response])),
        DerivedLevel("switch", Transition(response_switch, [response]))
    ])

    # Define sequence constraints
    k = 7
    constraints = [AtMostKInARow(k, resp_transition)]

    # Define experiment
    design       = [color, word, congruency, resp_transition, response]
    crossing     = [color, word, resp_transition]

    block = CrossBlock(design, crossing, constraints)

    # Solve
    if iteration == "initial":
        experiments  = synthesize_trials(block, 5, CMSGen)
    else:
        experiments  = synthesize_trials(block, 5, RandomGen(acceptable_error=3))

    # Convert experiments to dictionary format
    exp_block = experiments_to_dicts(block, experiments)
    timelines = experiments_to_dicts(block, experiments)

    timeline0 = pd.DataFrame.from_dict(timelines[0])
    return timelines


def run_experiment(timeline):
    # imports
    from sweetbean.stimulus import TextStimulus
    from sweetbean.sequence import Block

    # Creating the Instructions
    welcome = TextStimulus(
        text="Welcome to our experiment.<br />Here, you will have to react to the ink color of a color word.<br />Press SPACE to continue",
        choices=[' '])
    instruction_red = TextStimulus(
        text="If the ink color is <b>red</b>,<br />press <b>R</b> with your index finger as fast as possible.<br />Press R to continue",
        choices=['r'])
    instruction_green = TextStimulus(
        text="If the ink color is <b>green</b>,<br />press <b>G</b> with your index finger as fast as possible.<br />Press G to continue",
        choices=['g'])
    instruction_blue = TextStimulus(text="If the ink color is <b>blue</b>,<br />press <b>B</b> with your index finger as fast as possible.<br />Press B to continue",
                                    choices=['b'])
    instruction_yellow = TextStimulus(
        text="If the ink color is <b>yellow</b>,<br />press <b>Y</b> with your index finger as fast as possible.<br />Press Y to continue",
        choices=['y'])
    instructions_end = TextStimulus(
        text="The experiment will start now.<br />React as fast and as accurate as possible.<br />Remember:<br />React to the ink color not the meaning of the word.<br />Press SPACE to continue",
        choices=[' '])

    # Creating the stimulus sequence
    instructions_sequence = [welcome, instruction_red, instruction_green, instruction_blue, instruction_yellow, instructions_end]

    # Creating the block
    instructions_block = Block(instructions_sequence)

    # Import the functionality from sweetbean
    from sweetbean.parameter import TimelineVariable

    ## Declare the timeline variables

    # Color: The name has to be color (it is the name in the timeline), and it has the levels red, green, blue and yellow
    color = TimelineVariable(name="color", levels=["red", "green", "blue", "yellow"])

    # Word: The name has to be word (it is the name in the timeline), and it has the levels RED, GREEN, BLUE and YELLOW
    word = TimelineVariable(name="word", levels=["RED", "GREEN", "BLUE", "YELLOW"])


    # Importing the functionality
    from sweetbean.parameter import DerivedLevel

    # Declare the r level
    correct_response_r = DerivedLevel(value='r', predicate=is_correct_r, factors=[color])

    # Declare the j level
    correct_response_g = DerivedLevel('g', is_correct_g, [color])

    # Declare the b level
    correct_response_b = DerivedLevel('b', is_correct_b, [color])

    # Declare the y level
    correct_response_y = DerivedLevel('y', is_correct_y, [color])

    # Importing the functionality
    from sweetbean.parameter import DerivedParameter

    # Declare the "correct response" parameter
    correct_response = DerivedParameter(name='correct_response', levels=[correct_response_r, correct_response_g, correct_response_b, correct_response_y])

    # Imports
    from sweetbean.stimulus import TextStimulus

    # Declaring the stimulus
    stroop = TextStimulus(duration=2500, text=word, color=color, choices=['r', 'g', 'b', 'y'], correct_key=correct_response)

    # Import
    from sweetbean.parameter import DataVariable

    # Declare the data variable
    correct = DataVariable('correct', [True, False])

    positive_word_feedback = DerivedLevel('correct', is_positive_feedback, [correct], 1)
    negative_word_feedback = DerivedLevel('false', is_negative_feedback, [correct], 1)

    feedback_word = DerivedParameter('feedback_word', [positive_word_feedback, negative_word_feedback])
    # Create the levels
    positive_color_feedback = DerivedLevel('green', is_positive_feedback, [correct], 1)
    negative_color_feedback = DerivedLevel('red', is_negative_feedback, [correct], 1)
    # Create the parameter
    feedback_color = DerivedParameter('feedback_color', [positive_color_feedback, negative_color_feedback])
    feedback = TextStimulus(duration=1000, text=feedback_word, color=feedback_color)

    # Import the functionality from sweetbean to create experiments
    from sweetbean.sequence import Block, Experiment

    # Fixation stimulus
    fixation = TextStimulus(800, '+')

    # Create a stimulus sequence
    stimulus_sequence = [fixation, stroop, feedback]

    # Create the trial block
    trial_block = Block(stimulus_sequence, timeline)

    # Create the experiment from the two blocks
    experiment = Experiment([instructions_block, trial_block])
    print(experiment)

    # Construct the full path to the experimental.json file in the Downloads folder
    downloads_folder = os.path.expanduser('~/Downloads')
    experimental_file_path = os.path.join(downloads_folder, 'experimentData.json')

    # Check if the experimental.json file exists and delete it if it does
    if os.path.exists(experimental_file_path):
        os.remove(experimental_file_path)
        print(f"Deleted file: {experimental_file_path}")
    else:
        print(f"File not found: {experimental_file_path}")

    # export to the html file
    experiment.to_html('index.html')

    file_path = 'index.html'

    # Define the target string and the replacement string
    target_string = ''']
;jsPsych.run(trials)'''

    replacement_string = '''
    ,{
                type: jsPsychHtmlKeyboardResponse,
                stimulus: "<p>Thank you for participating!</p><p>Your responses have been recorded.</p><p>Press SPACE to finish.</p>",
                choices: [" "],
                on_finish: function() {
                    // Once the participant presses SPACE, we download the data
                    let data = jsPsych.data.get().json();
                    let blob = new Blob([data], { type: 'application/json' });
                    let url = URL.createObjectURL(blob);
                    let a = document.createElement('a');
                    a.href = url;
                    a.download = 'experimentData.json';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                }
            }]
    ;jsPsych.run(trials)
    '''

    # Open the file and read its contents
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace the target string with the replacement string
    modified_content = content.replace(target_string, replacement_string)

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)

    # Specify the path to your HTML file
    file_path = 'index.html'

    # Open the HTML file in the default web browser
    webbrowser.open('file://' + os.path.realpath(file_path))
