# Team MP2 13
Members: Ivan Alkhovik

## PDF
The PDF can be found at Alkhovik Mini-Project 2 Report.pdf.

## Code Organization
Code is written in Python and is broken up into 2 files for Question 1 and 2 (denoted in the name).

For Question 1, the code is divided into two sections. All this code is taken from the upwind scheme demo, but the first section is completely unedited, and the second has edits (separated by line of #'s). In the edited section, Solution1D has a new method which limits the min and max of a density to 0 and 160 respectively, impulse and the experiment methods are edited to fit the initial conditions given in the book, and bungwartz_upwind and step_lf2 are the stepper methods (which use the demo step_upwind and step_lf as references).

For Question 2, the show_grid method is taken from the cellular automata demo. Then, a grid is initialized (at first empty, then with vehicles which match the densities in Question 1). Finally, the stepper method updates the next row, by incrementing the speed's of the original row and shifting the vehicles by the speed.
