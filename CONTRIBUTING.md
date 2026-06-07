Contributing
============


Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

Code of Conduct
---------------

Everyone interacting in the getbibtex project's code base, issue tracker, and any communication channels is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).

Report Bugs
-----------

Report bugs at <https://github.com/goerz/getbibtex/issues>.

If you are reporting a bug, please include:

-   Your operating system name and version.
-   Any details about your local setup that might be helpful in troubleshooting.
-   Detailed steps to reproduce the bug, ideally a minimal but complete script or notebook.
-   All error messages in full, as plain text. If the output is long, attach it as a file.

Submit Feedback
---------------

The best way to send feedback is to file an issue at <https://github.com/goerz/getbibtex/issues>.

If you are proposing a feature:

-   Explain in detail how it would work.
-   Keep the scope as narrow as possible, to make it easier to implement.
-   Remember that this is a volunteer-driven project, and that contributions are welcome :)

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1.  The pull request should include tests.
2.  If the pull request adds functionality, the docs should be updated.
3.  Check <https://github.com/goerz/getbibtex/actions> and make sure that the tests pass for all supported Python versions.

Get Started!
------------

Ready to contribute? Follow [Aaron Meurer's Git Workflow Notes](https://www.asmeurer.com/git-workflow/) (with `goerz/getbibtex` instead of `sympy/sympy`)

In short,

1.  Clone the repository from `git@github.com:goerz/getbibtex.git`
2.  Fork the repo on GitHub to your personal account.
3.  Add your fork as a remote.
4.  Pull in the latest changes from the master branch.
5.  Create a topic branch.
6.  Make your changes and commit them (testing locally).
7.  Push changes to the topic branch on *your* remote.
8.  Make a pull request against the base master branch through the Github website of your fork.

The project uses [uv](https://docs.astral.sh/uv/) to manage the development environment and to run all development tasks such as testing and linting. See Development Prerequisites for details.

There is also a `Makefile` that wraps the common uv commands, for convenience. In your checked-out clone, run

~~~ console
make help
~~~

to see the available make targets. Each target runs through `uv run`, which automatically creates and synchronizes the development environment on first use; you can also set it up explicitly with `make develop`.

By default, tasks run against Python 3.12. To use a different interpreter, override the `PYTHON` variable, e.g. `make PYTHON=3.10 test`. uv downloads the requested interpreter automatically if it is not already installed.

Development Prerequisites
-------------------------

Contributing to the package's development requires only that you have [uv](https://docs.astral.sh/uv/) installed; follow the [uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/). uv manages the Python interpreters and all project dependencies for you, so there is no need to install Python or set up virtual environments manually. The project supports Python 3.10 and later.

Branching Model
---------------

For developers with direct access to the repository, getbibtex uses a simple branching model where all development happens directly on the `master` branch. All commits on `master` *should* pass all tests and be well-documented. This is so that `git bisect` can be effective. For any non-trivial issue, it is recommended to create a topic branch, instead of working on `master`. There are no restrictions on commits on topic branches, they do not need to contain complete documentation, pass any tests, or even be able to run.

To create a topic-branch named to address issue #1:

~~~ shell
git branch 1-title-of-issue
git checkout 1-title-of-issue
~~~

You can then make commits, and push them to Github to trigger Continuous Integration testing:

~~~ shell
git push -u origin 1-title-of-issue
~~~

Commit early and often! You are welcome to rewrite history on topic branches by force-pushing. Before submitting a pull request or merging into `master`, clean up the commit history of the topic branch.

-   Avoid having a series of meaningless granular commits like "start bugfix", "continue development", "add more work on bugfix", "fix typos", and so forth. Instead, use `git commit --amend` to add to your previous commit. This is the ideal way to "commit early and often". You do not have to wait until a commit is "perfect"; it is a good idea to make hourly/daily "snapshots" of work in progress. Amending a commit also allows you to change the commit message of your last commit.
-   You can combine multiple existing commits by "squashing" them. For example, use `git rebase -i HEAD~4` to combine the previous four commits into one. See the ["Rewriting History" section of Pro Git book](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History) for details (if you feel this is too far outside of your git comfort zone, just skip it).
-   You can use the `--fixup` flag for `git commit` to add to a previous commit. Fixup commits must be squashed (`git rebase --autosquash`) before merging.
-   If you work on a topic branch for a long time, and there is significant work on `master` in the meantime, periodically rebase your topic branch on the current master (`git rebase master`). Avoid merging `master` into your topic branch. See [Merging vs. Rebasing](https://www.atlassian.com/git/tutorials/merging-vs-rebasing).

If you are collaborating with others on a topic branch, coordinate with them before rewriting history.

When you are done with a topic branch (the issue has been fixed), finish up by merging the topic branch back into `master`:

~~~ shell
git checkout master
git merge --no-ff 1-title-of-issue
~~~

The `--no-ff` option is critical, so that an explicit merge commit is created (especially if you rebased). Summarize the changes of the branch relative to `master` in the commit message.

Then, you can push master and delete the topic branch both locally and on Github:

~~~ shell
git push origin master
git push --delete origin 1-title-of-issue
git branch -D 1-title-of-issue
~~~

Commit Message Guidelines
-------------------------

Write commit messages according to this template:

~~~ none
Short (50 chars or less) summary ("subject line")

More detailed explanatory text. Wrap it to 72 characters. The blank
line separating the summary from the body is critical (unless you omit
the body entirely).

Write your subject line in the imperative: "Fix bug" and not "Fixed
bug" or "Fixes bug." This convention matches up with commit messages
generated by commands like git merge and git revert. A properly formed
git commit subject line should always be able to complete the sentence
"If applied, this commit will <your subject line here>".

Further paragraphs come after blank lines.

- Bullet points are okay, too.
- Typically a hyphen or asterisk is used for the bullet, followed by a
  single space. Use a hanging indent.

You should reference any issue that is being addressed in the commit, as
e.g. "#1" for issue #1. If the commit closes an issue, state this on the
last line of the message (see below). This will automatically close the
issue on Github as soon as the commit is pushed there.

Closes #1
~~~

See [Closing issues using keywords](https://help.github.com/articles/closing-issues-using-keywords/) for details on references to issues that Github will understand.

Testing
-------

getbibtex includes a full test-suite using [pytest](https://docs.pytest.org/en/latest/). We strive for a [test coverage](https://codecov.io/gh/goerz/getbibtex) above 80%. Run `make coverage` to generate a local report (an HTML report in `./htmlcov` and an XML report in `coverage.xml`).

From a checkout of the `getbibtex` repository you can use

~~~ console
make test
~~~

to run the entire test suite against the default Python version. To run the tests against a specific interpreter, use e.g. `make PYTHON=3.10 test`. You can also verify the project against the lowest supported dependency versions with `make test-lowest`.

The tests are organized in the `tests` subfolder. It includes python scripts whose name start with `test_`, which contain functions whose names also start with `test_`. Any such functions in any such files are picked up by [pytest](https://docs.pytest.org/en/latest/) for testing. In addition, [doctests](https://docs.python.org/3.7/library/doctest.html) from any docstring or any documentation file (`*.rst` or `*.md`, such as this file and the `README.md`) are picked up (by the [pytest doctest plugin](https://docs.pytest.org/en/latest/doctest.html)).


Code Style
----------

All code must be compatible with [PEP 8](https://www.python.org/dev/peps/pep-0008/). The line length limit is 79 characters, although exceptions are permissible if this improves readability significantly.

Beyond PEP 8, this project adopts the [Black code style](https://github.com/psf/black/#the-black-code-style). You can run `make black-check` to check adherence to the code style, and `make black` to apply it. The version of `black` is pinned in `pyproject.toml` so that formatting stays reproducible across contributors.

Imports within python modules must be sorted according to the [isort](https://pycqa.github.io/isort/) configuration in `pyproject.toml`. The command `make isort-check` checks whether all imports are sorted correctly, and `make isort` modifies all Python modules in-place with the proper sorting.

The code style is enforced as part of the test suite, so please check your code before committing.
You may use `make flake8` and `make pylint` for additional checks on the code with [flake8](https://flake8.pycqa.org) and [pylint](https://pylint.pycqa.org), but there is no strict requirement for a perfect score with either one of these linters. They only serve as a guideline for code that might be improved. Running `make lint` performs all of the above checks together.
