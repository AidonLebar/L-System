# L-System
A program that produces and draws l-systems using PyOpenGl. See [the wikipedia article](https://en.wikipedia.org/wiki/L-system) 
on L-systems for a more in-depth description of what they are.

## Supported Grammar Rules
See dragon.txt for a very simple sample grammar. It should give you an idea of the format
1. The first section is the "axiom" or starting string
2. The second section contains the production rules for string rewriting
3. The third section contains the interpretation rules for the resulting string

### Production Rules
The following are examples of the different supported types of production rules:
* **Basic Rewrite** `A->B` Rewrite of A to B
* **Probabilistic Rewrite** `A(0.3)->B:C` rewite A to B with 30 percent probability else rewrite to C. 
Currently only binary outcomes are supported.
* **Context Sensitive Rewrite** `B<A>CC->D` rewrite A to D only if it follows a B and is followed by two Cs

### Interpretation Rules
The following are examples of the different supported types of interpretation rules:
* **Basic Interpretation** `A=forward` if A is encountered, move forward by default amount
* **Parametric Interpretation** `A=forward(12)` if A is encountered, move forward by 12

The current supported interepretation actions are:
* `forward` move forward
* `forward(x)` move forward by x
* `right` turn right 90 degrees
* `right(x)` turn right by x degrees
* `left` turn right 90 degrees
* `left(x)` turn right by x degrees
* `push` push position and location to a stack and turn right 90 degrees
* `push(x)` push position and location to a stack and turn right by x degrees
* `pop` pop position and location from stack and turn left 90 degrees
* `pop(x)` pop position and location from stack and turn left 90 degrees
* `colour(r,g,b)` change colour to specified RGB values (RGB ranges are 0-255)

## To Run
`python l_system.py <path to grammar file> <numberof genertions to compute>`

## Key Bindings
* `s` to save image to png format. The filename will be a timestamp.
* `<` go back one generation of rewrites
* `>` go forward one generation of rewrites
