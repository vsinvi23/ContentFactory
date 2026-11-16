# Git_and_Version_Control_Basics_for_Penetration_Testers

Source: https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Git and Git Version Control

Explore foundational Git version control commands critical for penetration testers. Understand how to clone repositories, stage changes, commit updates with messages, and push code to remote GitHub repositories. This lesson helps you manage and share your penetration testing tools efficiently.

We'll cover the following...

- [Introduction to Git and Git version control](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#Introduction-to-Git-and-Git-version-control)
  - [The git clone command](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#The-git-clone-command)
  - [The git add command](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#The-git-add-command)
  - [The git commit command](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#The-git-commit-command)
  - [The git push command](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#The-git-push-command)
  - [The add, commit, and push flow](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#The-add-commit-and-push-flow)

## Introduction to Git and Git version control[#](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#Introduction-to-Git-and-Git-version-control)

Git and Git version control concepts are necessary skills for any pentester in the field of information security. Growth in the field of penetration testing involves the development of small tools to automate tasks or make log checking more efficient. Such tools can be put on our own GitHub account to benefit others. They can also be obtained from other pentesters and developers who have their software available for free on GitHub. In either case, it’s important for a pentester to be able to apply the various Git commands to manage workflow and make life easier.

### The `git clone` command[#](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#The-git-clone-command)

The `git clone` command enables us to make a local copy of a repository. If the repository is public, then the command will work without problems.

Let’s assume we’d like to build the popular network mapping tool Nmap from the source. In order to do so, we first have to clone it. After ensuring we have Git installed on our system, all we need to do is go to the [Nmap](https://github.com/nmap/nmap) repository, click on “Code,” grab the HTTPS URL, and then use it with the following command in the terminal:

```
git clone <link here>
```

Terminal 1

Terminal

Click to Connect...

W

### The `git add` command[#](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#The-git-add-command)

The `git add` command adds new or changed files in our working directory to the Git staging area. It informs Git to include updates to particular files in the next commit.

### The `git commit` command[#](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#The-git-commit-command)

This command enables us to add comments to files regarding the changes that we’ve made in the files. It enables seamless collaboration between work groups in the writing of code or scripts in that the other person is able to know the different changes that have been made to the file.

It is normally applied after `git add`. We pass `-m` as an argument to the command, plus the comments on the changes that have been done to the files. We may be prompted by the terminal to configure the username and our password for the repository.

### The `git push` command[#](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#The-git-push-command)

This is a command that allows the user to update the code from the local to the remote repository. It allows users to be able to update the changes that they make in the different tasks that they are working on in the given GitHub environments.

### The `add`, `commit`, and `push` flow[#](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#The-add-commit-and-push-flow)

Using our cloned repository, which we cloned using the previous repository link, we will make a Python file in it with a name of our choice. We then push it to our GitHub repository. We need to make sure we configure our global email and global username for the final command, which is `git push`, to work.

We should create a GitHub account (if we don’t have one already) and test the following chain of commands to see how the previous Git commands work. We will also need to create a test repository through our GitHub account in order to follow along with the commands below.

```
git clone <your_repository_link>

cd <your_repository_folder>

touch test.txt

echo 'Hello World' >> test.txt

cat test.py

git add test.py

git config --global user.email "<your_email>"

git config --global user.name "<your_username>"

git commit -m "Added line to print Hello World"

git push -u origin main
```

Terminal 1

Terminal

Loading...

For more about Git and GitHub, refer to this [link](https://git-scm.com/book/en/v2) to get more information on optimizing Git workflows.

Text Manipulation

Software Management

Ask

[Introduction to Git and Git version control](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#Introduction-to-Git-and-Git-version-control)

[The git clone command](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#The-git-clone-command)

[The git add command](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#The-git-add-command)

[The git commit command](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#The-git-commit-command)

[The git push command](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#The-git-push-command)

[The add, commit, and push flow](https://www.educative.io/courses/web-application-penetration-testing/git-and-git-version-control#The-add-commit-and-push-flow)