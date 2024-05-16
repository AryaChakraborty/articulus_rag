# Contributing

Thanks for your interest in contributing! Please read carefully through our guidelines below to ensure that your contribution adheres to our project's standards.

## Code of Conduct

To hold a safe space for all contributors, we expect all project participants to adhere to our Code of Conduct. Please read the [full text](CODE_OF_CONDUCT.md) so that you can understand what actions will and will not be tolerated.

## Issue Tracking

We use [GitHub Issues](https://github.com/AryaChakraborty/articulus_rag/issues) to track all tasks related to this project.

## Build the project locally

In order to contribute to a project on GitHub, you must first get a copy of the project running locally on your computer. This process is sometimes called a "build process", and every project's process will have different requirements. Some requirements are due to the project being hosted on GitHub, some are due to the programming language used, some are due to the project's dependencies.

There are five steps to building this project:

1. [Set up Git and Install dependency](#set-up-git-and-install-nodejs)
1. [Fork the repository](#fork-the-repository)
1. [Clone your fork](#clone-your-fork)
1. [Install dependencies](#install-dependencies)
1. [Run the project](#run-the-project)


### Set up Git and Install dependeny

https://docs.github.com/en/get-started/getting-started-with-git/set-up-git

### Fork the repository

A *fork* is a copy of a repository. Forking a repository lets you to make changes to your copy without affecting any of the original code.

Click **Fork** (in the top-right corner of the page) to copy this repository to your GitHub account.

### Clone your fork

Cloning our fork lets you download a copy of the repository to your computer.

Use `git` to clone your fork

```
$ git clone https://github.com/YOUR-USERNAME/articulus_rag
```

### Install dependencies

First, navigate into the project's directory

```
$ cd articulus_rag
```

Next, use `pip` to install the project' dependencies
```
$ pip install requirements.txt
```

### Run the project

```
$ python app.py -mode
```

## Submit a Pull Request
 A *pull request* is a GitHub feature that lets you do just that!

There are three steps to submitting a pull request:
1. [Save your changes locally](#save-your-changes-locally)
2. [Send your changes to your fork](#send-your-changes-to-your-fork)
3. [Open a Pull Request](#open-a-pull-request)

These instructions are designed to explain the bare minimum steps in a beginner-friendly way.

### Save your changes locally

First, get a list of all the files you have changed.
```
$ git status
```

Next, *stage* the file you want to save. This will add the file to a new list that is ready to be saved.
```
$ git add .
```

Next, verify that the file has been staged correctly. Notice that the text color has changed, and your file is now in a list that says "Changes to be committed" instead of "Changes not staged for commit"
```
$ git status
```

Finally, save your staged files.
```
$ git commit -m "commit_message"
```

You'll often hear this process called *committing* changes. It's the exact same thing.

### Send your changes to your fork

With one simple `git` command, you can send the changes you just committed locally to your *fork* on GitHub.

```
$ git push origin master
```

### Open a Pull Request

1. Find the [New Pull Request](https://github.com/AryaChakraborty/articulus_rag/compare/) button
2. Select the option to **compare across forks**
3. Select **your username** in the `head fork` option
4. Select **your username** in the `base` option<sup>*</sup>
4. Click **Create Pull Request**

You can refer to the following articles on basics of Git and Github and also contact the Project Mentors, in case you are stuck:

## **Issue Report Process 📌**

1. Go to the project's issues.
2. Give proper description for the issues.
3. Don't spam to get the assignment of the issue 😀.
4. Wait for till someone is looking into it !.
5. Start working on issue only after you got assigned that issue 🚀.

# **Thank you for contributing💗** 
