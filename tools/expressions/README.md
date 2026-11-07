# Expression sheets

Renders many expressions of one character by timing four of them inside each 8 s clip,
then crops the stillest frame of each window. `expressions.py` holds the 48 expressions,
their facial cues and the 12-clip grouping; `sheet.py` does the work through `h3relay.py`.

    python sheet.py prep portrait.png        # pad to 1344x768 (or --size 960x544)
    python sheet.py prompts                  # review work/prompts/clipNN.txt
    python sheet.py submit --only 7          # test clip first
    python sheet.py submit                   # the rest
    python sheet.py crop                     # work/out/NN-name.png + contact-sheet.png

Crops are the square region the portrait was padded from; `work/out/full/` keeps whole frames.
