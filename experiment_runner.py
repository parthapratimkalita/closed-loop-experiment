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
- current color (red, blue, green, brown)
- current word (red, blue, green, brown)
- congruency (congruent, incongruent): Factor dependent on color and word.
- correct response (up, down, left right): Factor dependent on color.
- response Transition (repetition, switch). Factor dependent on response:

design:
- counterbalancing color x word x response Transition
- no more than 7 response repetitions in a row
- no more than 7 response switches in a row
"""


# DEFINE CONGRUENCY FACTOR
def congruent(color, word):
    return color == word


def incongruent(color, word):
    return not congruent(color, word)


# DEFINE RESPONSE FACTOR

def response_left(color):
    return color == 'red'


def response_right(color):
    return color == 'green'


# DEFINE RESPONSE TRANSITION FACTOR

def response_repeat(response):
    return response[0] == response[-1]


def response_switch(response):
    return not response_repeat(response)


# defining the predicate for the f-level of the "correct response" parameter
def is_correct_f(color):
    return color == 'red'

    # defining the predicate for the j-level of the "correct response" parameter


def is_correct_j(color):
    return color == 'green'


# positive feedback after correct responses (remember the correct data variable has boolean levels itself)
def is_positive_feedback(correct):
    return correct

    # negative feedback after incorrect responses


def is_negative_feedback(correct):
    return not correct


def sample_trials(iteration):
    from sweetpea import DerivedLevel

    # DEFINE COLOR AND WORD FACTORS

    color = Factor("color", ["red", "green"])
    word = Factor("word", ["red", "green"])

    conLevel = DerivedLevel("con", WithinTrial(congruent, [color, word]))
    incLevel = DerivedLevel("inc", WithinTrial(incongruent, [color, word]))

    congruency = Factor("congruency", [
        conLevel,
        incLevel
    ])

    response = Factor("correct_response", [
        DerivedLevel("f", WithinTrial(response_left, [color])),
        DerivedLevel("j", WithinTrial(response_right, [color])),
    ])

    resp_transition = Factor("response_transition", [
        DerivedLevel("repeat", Transition(response_repeat, [response])),
        DerivedLevel("switch", Transition(response_switch, [response]))
    ])

    # DEFINE SEQUENCE CONSTRAINTS

    k = 7
    constraints = [AtMostKInARow(k, resp_transition)]

    # DEFINE EXPERIMENT

    design = [color, word, congruency, resp_transition, response]
    crossing = [color, word, resp_transition]

    block = CrossBlock(design, crossing, constraints)

    # SOLVE

    if iteration == 'initial':
        experiments = synthesize_trials(block, 5, CMSGen)
    # Or:
    # experiments  = synthesize_trials(block, 5, IterateGen)
    # experiments  = synthesize_trials(block, 5, IterateILPGen)
    else:
        experiments = synthesize_trials(block, 5, RandomGen(acceptable_error=3))
    # experiments  = synthesize_trials(block, 5, RandomGen(acceptable_error=3))

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
        text="If the ink color is <b>red</b>,<br />press <b>F</b> with your left index finger as fast as possible.<br />Press F to continue",
        choices=['f'])
    instruction_green = TextStimulus(
        text="If the ink color is <b>green</b>,<br>press <b>J</b> with your right index finger as fast as possible.<br />Press J to continue",
        choices=['j'])
    instructions_end = TextStimulus(
        text="The experiment will start now.<br />React as fast an as accurate as possible.<br />Remember:<br />React to the ink color not the meaning of the word.<br />Press SPACE to continue",
        choices=[' '])

    # Creating the stimulus sequence
    instructions_sequence = [welcome, instruction_red, instruction_green, instructions_end]

    # Creating the block
    instructions_block = Block(instructions_sequence)

    # import the functionality from sweetbean
    from sweetbean.parameter import TimelineVariable

    ## declare the timeline variables

    # color: The name has to be color (it is the name in the timeline), and it has the levels red and green
    color = TimelineVariable(name="color", levels=["red", "green"])

    # word: The name has to be word (it is the name in the timeline), and it has the levels RED and GREEN
    word = TimelineVariable(name="word", levels=["RED", "GREEN"])

    # importing the functionality
    from sweetbean.parameter import DerivedLevel

    # declare the f level
    correct_response_f = DerivedLevel(value='f', predicate=is_correct_f, factors=[color])

    # declare the j level
    correct_response_j = DerivedLevel('j', is_correct_j, [color])

    # importing the functionality
    from sweetbean.parameter import DerivedParameter

    # declare the "correct response" parameter
    correct_response = DerivedParameter(name='correct_response', levels=[correct_response_f, correct_response_j])

    # imports
    from sweetbean.stimulus import TextStimulus

    # declaring the stimulus
    stroop = TextStimulus(duration=2500, text=word, color=color, choices=['j', 'f'], correct_key=correct_response)

    # import
    from sweetbean.parameter import DataVariable

    # declare the data variable
    correct = DataVariable('correct', [True, False])

    positive_word_feedback = DerivedLevel('correct', is_positive_feedback, [correct], 1)
    negative_word_feedback = DerivedLevel('false', is_negative_feedback, [correct], 1)

    feedback_word = DerivedParameter('feedback_word', [positive_word_feedback, negative_word_feedback])
    # create the levels
    positive_color_feedback = DerivedLevel('green', is_positive_feedback, [correct], 1)
    negative_color_feedback = DerivedLevel('red', is_negative_feedback, [correct], 1)
    # create the parameter
    feedback_color = DerivedParameter('feedback_color', [positive_color_feedback, negative_color_feedback])
    feedback = TextStimulus(duration=1000, text=feedback_word, color=feedback_color)

    # import the functionality from sweetbean to create experiments
    from sweetbean.sequence import Block, Experiment

    # fixation stimulus
    fixation = TextStimulus(800, '+')

    # create a stimulus sequence
    stimulus_sequence = [fixation, stroop, feedback]

    # create the trial block
    trial_block = Block(stimulus_sequence, timeline)

    # create the experiment from the two blocks
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
