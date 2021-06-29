# Comparison between search techniques
**Project developed in Ptyhon, using search algorithms **

## Search algorithms used
* UCS;
* A* (the option that gives all the way); 
* A* optimized (with open and closed lists, which gives only the minimum cost way);
* IDA*;

## The problem used for comparison

### Context
<div align="justify"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; N small frogs sat on a leaf. The frogs being very young, they still didn't know how to swim and they didn't like water and maybe that's why they really wanted to escape from the lake and reach the shore. The only way they could do this was to jump from leaf to leaf. 
<div align="justify"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The shape of the lake can be approximated to a circle. The coordinates of the leaves are related to the center of this circle (so the origin of the coordinate axes, ie the point (0,0) is in the center of the circle). 
<div align="justify"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Frogs jump from leaf to leaf. The length of a frog jump is the maximum weight / 3. Due to the effort, the frog loses one unit of energy (weight) with each jump. It is considered that weight loss occurs during the jump, so when it reaches its destination it already has one unit less. If a frog reaches a weight of 0, then it dies. 
<div align="justify"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; On some leaves there are insects, on others not. When the frog arrives on a leaf it eats a part (a number between 0 and how many insects are found on the leaf) of the insects found and this gives it energy for new jumps. The input file will specify the number of insects found on each leaf. If the frog eats an insect, it gains weight by one unit. Once it has eaten some of the insects on a leaf, the leaf remains without that number of insects. 
<div align="justify"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Each leaf has a maximum accepted weight. The weight on a leaf is given by the weight of the insects added to that of the frogs (there may be more on one leaf).

### States and transitions
<div align="justify"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Although all jumps are treated as a single move, in performing calculations on weights and insects, frogs jump in order according to their index. The nodes are not created for each frog, but for all the jumps at the same time.
<div align="justify"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; A transition is considered to be the consumption of insects on the leaf on which it is located plus a jump on another leaf.



 
