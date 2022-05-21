# Sudoku Algorithms

## About

This repository is intended to document the implementation and comparison of three deterministic algorithms to solve a classic 9x9 sudoku.

## Algorithms

<h3><a href="/algorithms/bf.py">Simple Backtracking (SB)</a></h3>

Simple backtracking is perhaps the simplest sudoku solving algorithm, and serves as a baseline for the other algorithms. It entails iterating over the sudoku grid and assigning valid values to unfilled cells (a value is considered valid if there is no other cell with the same value in the row/column/3x3 box of the given cell). In case assignments lead to an unfeasible scenario, the algorithm backtracks and attempts alternative assignments to the unfilled cells. 

<h3><a href="/algorithms/csp.py">Constraint Satisfaction Problem (CSP)</a></h3>

Simple backtracking can be enhanced when modelling the sudoku as a <a href="https://en.wikipedia.org/wiki/Constraint_satisfaction_problem">constraint satisfaction problem (CSP)</a>. Of particular significance is the <b>Maintaining Arc Consistency (MAC) algorithm</b>, which trims the set of possible values for other unfilled cells whenever an unfilled cell is assigned. Additionally, the choice of the next unfilled cell to assign can be made more efficient via the <b>minimum-remaining-values (MRV) heuristic</b> (choose the unfilled cell with the fewest possible values) and the <b>degree heuristic</b> (choose the unfilled cell that is involved in the largest no. of constraints with other unfilled cells).

(See for reference Chapter 6 of Russell, S. J., Norvig, P., & Davis, E. (2010). Artificial intelligence: a modern approach. 3rd ed. Upper Saddle River, NJ: Prentice Hall)

<h3><a href="/algorithms/dlx.py">Algorithm X (DLX)</a></h3>

The sudoku can be modelled as an <a href="https://en.wikipedia.org/wiki/Exact_cover">exact cover problem</a>, which lends itself to solving via the <a href="https://en.wikipedia.org/wiki/Dancing_Links">dancing links</a> implementation of <a href="https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X">Donald Knuth's Algorithm X</a>.

(See for reference https://arxiv.org/pdf/cs/0011047.pdf)

## Comparison

We define the <b>no. of guesses</b> made by an algorithm as the no. of times it attempts to assign a value to an unfilled cell when solving a sudoku. We note that the term "guess" is applied loosely here, as any attempt to assign a value to an unfilled cell would be considered a guess, even if the algorithm is certain of what value is to be assigned. Regardless, given that all algorithms are faced with the same no. of unfilled cells, the no. of guesses serves as a rough metric to compare algorithm performance. 

The algorithms are compared using two data sources below.

### NYTimes Sudoku Dataset

NYTimes publishes easy, medium, and hard classic 9x9 sudokus daily. We consider a <a href="/comparison/NYTimes_Sudoku_Dataset.csv">dataset</a> of 125 sudokus of each difficulty level (compiled by me over the period Jun 1 to Oct 3 of 2021) to compare the algorithms.

The following table shows the average no. of unfilled cells for each difficulty level. Interestingly, all 125 easy sudokus had exactly 43 unfilled cells. Additionally, given that both the medium and hard sudokus had a roughly similar average unfilled count (~ 57), the key factor separating medium sudokus from hard sudokus seems to be the arrangement of unfilled cells (as opposed to their count). 

<div align="center">
<table>
    <tr>
        <th>Difficulty</th>
        <th>Average Unfilled Count</th>
    </tr>
    <tr>
        <td>Easy</td>
        <td>43.00</td>
    </tr>
    <tr>
        <td>Medium</td>
        <td>57.06</td>
    </tr>
    <tr>
        <td>Hard</td>
        <td>57.15</td>
    </tr>
</table>
</div>

The following table shows the average no. of guesses for each case.

<div align="center">
<table>
    <tr>
        <th>Difficulty</th>
        <th>Algorithm</th>
        <th>Average no. of guesses</th>
    </tr>
    <tr>
        <td>Easy</td>
        <td>Simple Backtracking</td>
        <td>96.46</td>
    </tr>
    <tr>
        <td>Easy</td>
        <td>Constraint Satisfaction Problem</td>
        <td>43.01</td>
    </tr>
    <tr>
        <td>Easy</td>
        <td>Algorithm X</td>
        <td>43.00</td>
    </tr>
    <tr>
        <td>Medium</td>
        <td>Simple Backtracking</td>
        <td>132818.38</td>
    </tr>
    <tr>
        <td>Medium</td>
        <td>Constraint Satisfaction Problem</td>
        <td>186.59</td>
    </tr>
    <tr>
        <td>Medium</td>
        <td>Algorithm X</td>
        <td>69.95</td>
    </tr>
    <tr>
        <td>Hard</td>
        <td>Simple Backtracking</td>
        <td>227502.38</td>
    </tr>
    <tr>
        <td>Hard</td>
        <td>Constraint Satisfaction Problem</td>
        <td>198.81</td>
    </tr>
    <tr>
        <td>Hard</td>
        <td>Algorithm X</td>
        <td>91.71</td>
    </tr>
</table>
</div>

Additionally, boxplots of the no. of guesses for each case are shown below. There is one plot for each difficulty level. Within each plot, separate boxplots are provided for each algorithm.

<p align="center">
    <img src="/comparison/sb, csp, dlx.png" alt="BF, CSP, DLX">
</p>

We note the following :-

<ul>
    <li>The DLX algorithm outperforms the CSP algorithm, which in turn outperforms the SB algorithm.</li>
    <li>Given that there are 43 unfilled cells for each easy sudoku and the CSP and DLX algorithms are making ~ 43 guesses on average, these two algorithms are getting essentially all assignments right on first try.</li>
    <li>The SB algorithm has comparable performance to the other two algorithms for easy sudokus. However, unlike the other two algorithms, its performance scales atrociously when increasing the sudoku difficulty level.</li>
</ul>

Now, for a clearer comparison of the CSP and DLX algorithms, we consider the boxplots after excluding the SB algorithm. These are shown below.

<p align="center">
    <img src="/comparison/csp, dlx.png" alt="CSP, DLX">
</p>

We note that in addition to having a lower average no. of guesses compared to the CSP algorithm, the DLX algorithm seems to be more robust to variations in sudoku design for any given difficulty, as it has a much lower spread in the no. of guesses compared to the CSP algorithm.

### Al Escargot ("The Most Difficult Sudoku Puzzle")

We consider the famous Al Escargot, known for being the most difficult sudoku puzzle in 2006. The grid with only prefilled cells is shown below.

<p align="center">
    <img src="/comparison/al_escargot.png" alt="Al Escargot" width="50%" height="50%">
</p>

The following table shows the no. of guesses made by each algorithm for Al Escargot. We note that Al Escargot seems to live upto its name, as the no. of guesses for the CSP and DLX algorithms here is signficantly in excess of the average no. of guesses for these two algorithms for the hard NYTimes sudokus.

<div align="center">
<table>
    <tr>
        <th>Algorithm</th>
        <th>No. of guesses</th>
    </tr>
    <tr>
        <td>Simple Backtracking</td>
        <td>49558</td>
    </tr>
    <tr>
        <td>Constraint Satisfaction Problem</td>
        <td>4051</td>
    </tr>
    <tr>
        <td>Algorithm X</td>
        <td>1471</td>
    </tr>
</table>
</div>
