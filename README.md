
# Lox Tree-Walk Interpreter in Python

I'm following along with the wonderful book [Crafting Interpreters](https://craftinginterpreters.com/),
and using this repo for my implementation of the Lox tree-walk interpreter. Because I didn't want to
setup a JDK, I am using Python.

Overall my opinion of the code samples in the book is that they tend to be a bit overly verbose and 
class-y. This is unavoidable with Java code. I've tried to respect Mr Nystrom's names were possible.

This is still a WIP, there is no actual interpreting yet. I am trying to annotate commits with relevant
book chapters.

## How to Run

This code has no runtime dependencies outside of a not-ancient `python3` install. The `requirements.txt`
has dev dependencies, for linting etc.

`python py/main.py` for the repl.

## Disclaimer

Low comments, low tests. Not really a python guy outside of hacky oneoff scripts, so not really sure
about any best practice.
