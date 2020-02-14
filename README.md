# Project ET zero

ASRT script used in projet ET zero.

The core ASRT scirpt is implemented here:
https://github.com/tzolnai/asrt_core

### Prerequisites
Running ASRT script requires all of the following and their dependencies.

* [Python 3.6](https://www.python.org/downloads/)
* [Tobii Pro SDK](https://pypi.org/project/tobii-research/) (only for eye-tracking)
* [PsychoPy](https://www.psychopy.org/download.html)
* [pyglet](https://pyglet.readthedocs.io/en/stable/)

After Python 3.6 and pip is intalled, you can install psychopy, tobii_research and pyglet packages using `pip install`.
This ASRT script uses an older version of pyglet (<=1.3.2) so for pyglet you need to specify the version explicitely:
```
pip install pyglet==1.3.2
```

Additional dependencies (for development):
* [pytest](https://docs.pytest.org/en/latest/): For running tests under test folder
* [pynput](https://pypi.org/project/pynput/): For running ET_simulation script (dev_tools folder)
* [autopep8](https://pypi.org/project/autopep8/): For running autoformat script (dev_tools folder)

### Setup

After all prerequisites are installed you need to download the content of this repository.

Before running the ASRT script you need to place an instruction file in the same folder where the `asrt.py` is.
The instruction file should have the name `inst_and_feedback.txt`. You can find example instruction files under `inst_examples` folder.

When instruction file is in place you can run the script by `python asrt.py` command or by running the `asrt.py` file from PsychoPy.

### References

I-DT: Dispersion-Threshold identification of fixations:

* [Salvucci, D. D., & Goldberg, J. H. (2000, November). Identifying fixations and saccades in eye-tracking protocols.
In Proceedings of the 2000 symposium on Eye tracking research & applications (pp. 71-78).](https://www.researchgate.net/publication/220811146_Identifying_fixations_and_saccades_in_eye-tracking_protocols)

* [Blignaut, P. (2009). Fixation identification: The optimum threshold for a dispersion algorithm. Attention, Perception, & Psychophysics, 71(4), 881-895.](https://link.springer.com/article/10.3758/APP.71.4.881)

* [Blignaut, P., & Beelders, T. (2009). The effect of fixational eye movements on fixation identification with a dispersion-based fixation detection algorithm.](https://www.researchgate.net/publication/297523424_The_effect_of_fixational_eye_movements_on_fixation_identification_with_a_dispersion-based_fixation_detection_algorithm)
