# Project Starter — Fall 2026

This repository provides the framework needed to develop and run the Fall 2026
CS 131 interpreter projects.

## Notes

- Your project must have a top-level, versioned `interpretervX.py` file, where
  `X` is the current project number. That file must export the `Interpreter`
  class or it will not run on the autograder.
- You may find the spec for the given project under the `pXspec` directory.
- Your Gradescope submission should contain `interpretervX.py` and any
  additional files you wrote that it relies on. Do not submit the base files.
- Maintain a copy of your local Git history and commit regularly as you work.
  Although this is not required for submission, we reserve the right to ask for
  it if we suspect foul play.
- A few days after each project deadline, we will upload a reference solution
  to this repository. We recommend building the next part on your own code, but
  you may instead build on the prior project's reference solution.
- Use Python 3.11 or newer. Older versions may produce unexpected issues.

### Framework files

The following files provide the parser and runtime framework:

```text
ply/lex.py
ply/yacc.py
brewlex.py
brewparse.py
element.py
intbase.py
```

You do not need to understand these files beyond the documented methods used by
the projects, and you should not modify them.

## Local autograder

When public tests are added under `vX/tests` and `vX/fails`, run them with:

```shell
python tester.py <project number>
```

The local autograder automatically includes any additional `.br` tests you add
to the corresponding directories.

## Licensing and attribution

This is an unlicensed repository. Even though its source code is public, it is
not governed by an open-source license.

This code was primarily written by
[Carey Nachenberg](http://careynachenberg.weebly.com/) with support from his
teaching assistants.
