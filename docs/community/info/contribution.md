# Contributing Code

---
## Creating a PR
We welcome anyone to contribute code to VeighNa.

If you wish to contribute code, please use the GitHub PR (Pull Request) process.

The PR process is roughly as follows:

---
1. [Create Issue][CreateIssue] - For larger changes (such as new features, major refactoring, etc.), it is recommended to open an issue first for discussion. For smaller improvements (such as documentation improvements, bugfixes, etc.), you can directly submit a PR.

2. Fork [VeighNa][#GithubVnpy] - Click the **Fork** button in the upper right corner

3. Clone your fork: ```git clone https://github.com/$userid/vnpy.git```

	> If your fork is out of date, you need to manually [sync][GithubDocForSync]

4. Create your own branch from **dev**: ```git checkout -b $my_feature_branch dev```

5. Make changes on $my_feature_branch and push the changes to your forked repository

6. Create a [Pull Request] from your fork's $my_feature_branch branch to the main project's **dev** branch:
 [Click here][CreatePR], then click **compare across forks**, select the required fork and branch to create the PR

---

After creating the PR, please wait patiently: we will check the PR as soon as we have time. Once your code is useful and [meets the requirements](#code-style), it will be merged!


---
## Code Style
When writing code for VeighNa, you need to follow some basic rules, otherwise your code may not be merged.
These rules include:
- [Contributing Code](#contributing-code)
  - [Creating a PR](#creating-a-pr)
  - [Code Style](#code-style)
    - [Naming Conventions](#naming-conventions)
    - [Code Format](#code-format)
    - [Code Quality Checks](#code-quality-checks)


### Naming Conventions
Our code naming rules are as follows:

* Class properties, class methods, parameters, and variables should use lowercase with underscores
* Class names should use camelCase naming
* Constants should use uppercase with underscores

For example:
```python3
DEFAULT_PATH = "/tmp/VeighNa/"
class ClassA:
    def __init__(self, arg_one: int, arg_two: str):
        if arg_two is None:
            arg_two = DEFAULT_PATH
        self.property_one = arg_one
        variable_one = "some string"
```


### Code Format
We don't have particularly strict requirements for code format, but it must at least conform to the pep8 standard, and additionally you must include docstrings (a """ """) under classes and functions.

To make your code conform to the pep8 standard, use [autopep8](https://github.com/hhatto/autopep8) to format your code after writing it:
```bash
autopep8 --in-place --recursive .
```

### Code Quality Checks
The VeighNa project uses two tools to ensure code quality:

1. [ruff](https://github.com/astral-sh/ruff) - For code style and quality checks
   - Run ```ruff check .``` in the project root directory to check for style issues in the code
   - You can use ```ruff check --fix .``` to automatically fix some issues

2. [mypy](https://github.com/python/mypy) - For static type checking
   - Run ```mypy vnpy``` in the project root directory to check for type annotation issues in the code

If errors or warnings are detected, it means your code needs to be modified to meet the project standards. Make sure to resolve all warnings and errors before submitting a PR.

[GithubVnpy]:https://github.com/vnpy/vnpy
[GithubDocForSync]:https://help.github.com/articles/syncing-a-fork/
[CreateIssue]:https://github.com/vnpy/vnpy/issues/new
[CreatePR]:https://github.com/vnpy/vnpy/compare?expand=1

