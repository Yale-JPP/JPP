# Contains all parameters that can be adjusted to affect grading/the way algorithms work.

# ~~~~~~~~~~~ PARAMETERS THAT AFFECT WHISPER ~~~~~~~~~~~
SELECTED_MODEL = "base" # model type used for whisper. one of "tiny", "base", "small", "medium", and "large".

# ~~~~~~~~~~~ PARAMETERS THAT AFFECT THE GRADE CALCULATION ~~~~~~~~~~~
BASE_GRADE = 50 # the starting point for a non-zero coefficient grade
CORRECT_LANGUAGE_WEIGHT = 0.6 # weight given to an answer that gets the correct language detected.
CORRECT_TEXT_WEIGHT = 0.4 # weight given to an answer that gets the correct input text detected.
HIRAGANA_NOT_FOUND_PENALTY = 0.9 # penalty coefficient to which a grade should be multiplied if an expected hiragana is not found.

# ~~~~~~~~~~~ PARAMETERS THAT AFFECT THE AUDIO ANALYSIS ~~~~~~~~~~~
BUF_SIZE = 1024 # higher value means more frequency resolution
HOP_SIZE = 128 # lower value means larger rate of sampling
PITCH_TOLERANCE = 0.8