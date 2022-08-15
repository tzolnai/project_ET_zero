# Project ET Zero

ASRT script used in projet ET zero.

The core ASRT script is implemented here:
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

### Credits

Maintainer: **Tamás Zolnai** ([tzolnai](https://github.com/tzolnai))

This code is forked from this github repository: https://github.com/hallgatoemese/asrt.

The original codes' author is **Emese Szegedi-Hallgató** ([hallgatoemese](https://github.com/hallgatoemese))

The code was rewritten and was extended with eye-tracker capabilities by **Tamás Zolnai** ([tzolnai](https://github.com/tzolnai))

### Citation

Project ET Zero Developers (2021). Project ET Zero (Version 0.1.1) [Computer software].

### Example data

Recorded data by this experiment script (2022):
https://osf.io/wu8a6/

### Study conducted based on this script 

* [Zolnai, T., Dávid, D., Pesthy, O., Nemeth, M., Kiss, M., Nagy, M., & Nemeth, D. (2022). Measuring statistical learning by eye-tracking. Experimental Results, 3, E10. doi:10.1017/exp.2022.8](https://www.cambridge.org/core/journals/experimental-results/article/measuring-statistical-learning-by-eyetracking/03CE0A705EAB7708AB087554A74A29F1)

### References

ASRT (alternating SRT, alternating serial reaction time task)

* [Howard Jr, J. H., & Howard, D. V. (1997). Age differences in implicit learning of higher order dependencies in serial patterns. Psychology and aging, 12(4), 634.](https://www.researchgate.net/profile/James_Howard11/publication/13812889_Age_differences_in_implicit_learning_of_higher_order_dependencies_in_serial_patterns/links/0deec52423cfe984b4000000.pdf)

* [Kóbor, A., Janacsek, K., Takács, Á., & Nemeth, D. (2017). Statistical learning leads to persistent memory: Evidence for one-year consolidation. Scientific reports, 7(1), 1-10.](https://www.nature.com/articles/s41598-017-00807-3?WT.feed_name=subjects_biological-sciences)

* [Simor, P., Zavecz, Z., Horvath, K., Éltető, N., Török, C., Pesthy, O., ... & Nemeth, D. (2019). Deconstructing procedural memory: Different learning trajectories and consolidation of sequence and statistical learning. Frontiers in psychology, 9, 2708.](https://www.frontiersin.org/articles/10.3389/fpsyg.2018.02708/full)

I-DT: Dispersion-Threshold identification of fixations

* [Salvucci, D. D., & Goldberg, J. H. (2000, November). Identifying fixations and saccades in eye-tracking protocols.
In Proceedings of the 2000 symposium on Eye tracking research & applications (pp. 71-78).](https://www.researchgate.net/publication/220811146_Identifying_fixations_and_saccades_in_eye-tracking_protocols)

Dispersion threshold

* [Blignaut, P. (2009). Fixation identification: The optimum threshold for a dispersion algorithm. Attention, Perception, & Psychophysics, 71(4), 881-895.](https://link.springer.com/article/10.3758/APP.71.4.881)

* [Blignaut, P., & Beelders, T. (2009). The effect of fixational eye movements on fixation identification with a dispersion-based fixation detection algorithm.](https://www.researchgate.net/publication/297523424_The_effect_of_fixational_eye_movements_on_fixation_identification_with_a_dispersion-based_fixation_detection_algorithm)

Fixation duration threshold

* [Manor, B. R., & Gordon, E. (2003). Defining the temporal threshold for ocular fixation in free-viewing visuocognitive tasks. Journal of neuroscience methods, 128(1-2), 85-93.](https://www.sciencedirect.com/science/article/pii/S0165027003001511)

Linear interpolation of missing data

* [Olsen, A. (2012). The Tobii I-VT fixation filter. Tobii Technology, 1-21.](https://stemedhub.org/resources/2173/download/Tobii_WhitePaper_TobiiIVTFixationFilter.pdf)

Jacobi PDP test

* [Jacoby, L. L. (1991). A process dissociation framework: Separating automatic from intentional uses of memory. Journal of memory and language, 30(5), 513-541.](https://www.sciencedirect.com/science/article/abs/pii/0749596X9190025F)

* [Destrebecqz, A., & Cleeremans, A. (2001). Can sequence learning be implicit? New evidence with the process dissociation procedure. Psychonomic bulletin & review, 8(2), 343-350.](https://link.springer.com/article/10.3758/BF03196171)

* [Kóbor, A., Janacsek, K., Takács, Á., & Nemeth, D. (2017). Statistical learning leads to persistent memory: Evidence for one-year consolidation. Scientific reports, 7(1), 1-10.](https://www.nature.com/articles/s41598-017-00807-3?WT.feed_name=subjects_biological-sciences)

Oculomotor activation

* [Vakil, E., Bloch, A., & Cohen, H. (2017). Anticipation measures of sequence learning: manual versus oculomotor versions of the serial reaction time task. The Quarterly Journal of Experimental Psychology, 70(3), 579-589.](https://journals.sagepub.com/doi/pdf/10.1080/17470218.2016.1172095?casa_token=YLxCT1H_B8cAAAAA:6kFyQ1yW1qfe2NZP-mSdfLnAVxLDIal-QaF4siYPOz5wRb-d9zgr5IyrYGS44O47wOImxUf_PEMZ1Q)

Technical documentation

* [Accuracy and precision Test report Tobii Pro X3-120 fw 1.7.1](https://www.tobiipro.com/siteassets/tobii-pro/accuracy-and-precision-tests/tobii-pro-x3-120-accuracy-and-precision-test-report.pdf)

* [Tobii Pro Python SDK reference](http://developer.tobiipro.com/python/python-sdk-reference-guide.html)

* [Tobii Pro X3–120 Eye Tracker: Product Description](https://www.tobiipro.com/siteassets/tobii-pro/product-descriptions/tobii-pro-x3-120-product-description.pdf)

