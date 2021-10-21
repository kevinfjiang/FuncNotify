# Contributing ⏰ 
> **How to Contribute**

#### Conribution Guide:
1. ⭐⭐ Give us a Star on GitHub ⭐⭐
2. Fork the repository into your account
3. Clone your repository into your working drive `git clone [url in green code dropdown]`
   a. Replace anything in `[anything]` in brackets
4. Please follow the instructions in `FuncNotify/TemplateMethod_.py` and add to `template.env` and create a new branch. Also let me know of any more credentials so I can add them to testing
   a. Just add a file called `[Method_Name]Method.py` and a decorator called `def time_[Method_Name]():`, and a `test_[Method_Name].py` for tests.
   b. Add any additional packages to `requirements.txt`, this allows me to dynamically track every package necessary so builds are easier
5. REACH OUT to me at `kevin.j@columbia.edu` for help or issues.

#### Abstract Class and Automated implementation:
Make sure any Class you must inherit from the Abstract Class `NotifyMethods` via `class [Method_Name]Method(NotifyMethods):`. Then implement the methods found in `TemplateMethod_.py` for the correct methods. Look at other files for the proper format.

All classes will automatically added to a dictionary that can be accessed with a string as a key `"[Method_Name]"`. Pass that string as an argument to get notified via that method.

Ideally, please stay within the design principless of the class so the automation I set up still works. Other than that, there are no realy constraints on how to solve isssues. This project ideally helpss users get familiar with enterprise APIs and learn some cool tricks while doing it.

#### Comments:
Try and write as detailed comments on **why** things happen. Try and write code that is self-explanatory, without too many comments. Try and keep the same format of docstrings for each new method. Check out this link for a VsCode extension to automatically create docstrings

#### Describe your changes well.
> **skim this git guide, you don't *really* have to follow lol**

The first line of the commit message should be a short description (50
characters is the soft limit, see DISCUSSION in git-commit(1)), and
should skip the full stop.  

* push: allow pushing to multiple remotes

* grep: allow passing in command-line arguments

If in doubt which identifier to use, run "git log --no-merges" on the
files you are modifying to see the current conventions.

The body should provide a meaningful commit message, which:

* explains the problem the change tries to solve, iow, what is wrong
  with the current code without the change.

* justifies the way the change solves the problem, iow, why the
  result with the change is better.

* alternate solutions considered but discarded, if any.

#### Testing:
Create a copy of the `template.env` and name it `.env` and fill it out with your full credentials for full scale testing.

For writing your own tests, create your own file called `test_[Method_Name].py` and create a class that inherits from TestGeneric `class Test[Method_name](TestAbstract)`. Implement the `@abstractmethods` according to the templates and usse the other methods in the class `TestAbstract`. Enable/disable tests with `__test__=False` (Note, this a default unittest feature but I had to do some metaclass stuff to make it work somehow)

