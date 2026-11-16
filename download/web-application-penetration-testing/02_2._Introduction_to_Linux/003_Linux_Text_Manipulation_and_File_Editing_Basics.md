# Linux_Text_Manipulation_and_File_Editing_Basics

Source: https://www.educative.io/courses/web-application-penetration-testing/text-manipulation

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Text Manipulation

Explore fundamental Linux text manipulation techniques including file and folder creation and removal. Learn how to view, append, and edit files using commands like cat and echo. Gain practical skills with the Vim editor, mastering insert and command modes to efficiently edit text files within Linux environments.

We'll cover the following...

- [Introduction to text manipulation](https://www.educative.io/courses/web-application-penetration-testing/text-manipulation#Introduction-to-text-manipulation)
- [Creating files and folders](https://www.educative.io/courses/web-application-penetration-testing/text-manipulation#Creating-files-and-folders)
- [Removing files and folders](https://www.educative.io/courses/web-application-penetration-testing/text-manipulation#Removing-files-and-folders)
- [Viewing and appending data to files](https://www.educative.io/courses/web-application-penetration-testing/text-manipulation#Viewing-and-appending-data-to-files)
- [Vim editor](https://www.educative.io/courses/web-application-penetration-testing/text-manipulation#Vim-editor)

## Introduction to text manipulation[#](https://www.educative.io/courses/web-application-penetration-testing/text-manipulation#Introduction-to-text-manipulation)

This lesson introduces multiple ways of manipulating text in files. We will also be looking into file and folder creation.

## Creating files and folders[#](https://www.educative.io/courses/web-application-penetration-testing/text-manipulation#Creating-files-and-folders)

We can create a folder using `mkdir`, which is a utility for the creation of directories in the Linux system. Simply provide a name for the new directory with `mkdir`, and we’re good to go.

We can use the `touch` command for file creation, though it can also be used to modify the timestamps of files and directories. Again, we simply provide the name and extension for the file we’d like to create.

The terminal below shows how we create a new folder called `world` and then create a text file inside it called `hello.txt`.

Terminal 1

Terminal

Click to Connect...

W

## Removing files and folders[#](https://www.educative.io/courses/web-application-penetration-testing/text-manipulation#Removing-files-and-folders)

We can remove files and folders with the `rm` command. To remove individual files, simply provide their name with the command. Removing folders is slightly trickier; empty folders require the `-d` option, while non-empty folders require the `-r` option. The latter option recursively removes everything inside the folder.

Let’s test these new commands in the terminal below:

Terminal 1

Terminal

Loading...

## Viewing and appending data to files[#](https://www.educative.io/courses/web-application-penetration-testing/text-manipulation#Viewing-and-appending-data-to-files)

The concatenation command, which is denoted as `cat`, is used to display the contents of a file. However, the command can also help in the creation of small files and appending new content to them.

Assume we have an empty text file called `empty.txt`. We can verify that it’s empty with `cat empty.txt`.

Now let’s create a basic text file called `introduction.txt` and have it contain “Hello world!” We can do so with `cat &gt; introduction.txt`. The file will be created, and the terminal will go into interactive mode. We can then add the required text and exit the mode by pressing “CTRL+D.” We can then append more text (let’s append " Goodbye world…") to the file using `cat &gt;&gt; introduction.txt`.

While the `echo` command is primarily used in Bash scripting and debugging, we can also use the `echo` command to write reasonably small data to files. For example, to repeat what was discussed with `cat`, we would do the following:

```
echo 'Hello world! Goodbye world...' &gt; introduction.txt
```

Practice makes perfect so try these commands in the terminal below before proceeding forward. Note that `empty.txt` already exists. The output of the final `introduction.txt` should be “Hello world! Goodbye world…”

Terminal 1

Terminal

Loading...

## Vim editor[#](https://www.educative.io/courses/web-application-penetration-testing/text-manipulation#Vim-editor)

Vim is an editor that usually comes preinstalled on Linux systems for text manipulation. Examples of other text editors include Elvis, nvi, nano, and Vile.

For this course, we will learn and use Vim because the editor is rich in features and is perfect for quickly editing files when necessary. Since it usually comes preinstalled, pentesters are expected to know its basics because, oftentimes, installation of new software isn’t allowed.

Vim operates in two modes as discussed below:

- **Command mode:** Enter the Vim CLI for administrative tasks. It enables us to save, move the cursor, cut, paste, etc.
- **Insert mode:** Insert text into or remove text from a file within the Vim CLI.

Now let’s dive into using Vim. We can initiate it by just typing `vim` on the command line and it will open in command mode.

Here are some of the key Vim commands that we’ll be using most frequently:

- `i`: Switch to insert mode.
- `a`: Write after the cursor and switch to insert mode.
- `A`: Write at the end of the line and switch to insert mode.
- `Esc`: Terminate insert mode.
- `u`: Undo the last change in a file.
- `U`: Undo changes made to an entire line.
- `o`: Open a new line and switch to insert mode.
- `dd`: Delete a line.
- `3dd`: Delete three lines in the editor.
- `D`: Delete everything from where the cursor is to the end of the line.
- `C`: Delete the contents of a line after the cursor, after which it switches to insert mode.
- `dw`: Delete a word in the editor.
- `4dw`: Delete four words in the editor.
- `cw`: Change a word in the editor.
- `x`: Delete characters at the cursor in the editor.
- `r`: Replace a character in the editor.
- `R`: Overwrite characters from the cursor onward in a line in the editor.
- `s`: Substitute one character under the cursor and switch to insert mode.
- `S`: Substitute an entire line by beginning to insert text at the beginning of that line.
- `~`: Change the case of an individual character.
- “Shift + : + q”: Quit the editor
- “Shift + : + wq”: Quit the editor by saving whatever text has been inserted in the editor when it was in insert mode.

Try out the commands above in the terminal below to get a better grasp of Vim. First, try editing a simple file that contains the “Hello World” greeting. Save it, and then append a response, a “Goodbye world” message, to it. Last, change the order of the two lines so that the previously appended line now comes first. The file to edit, called `text.txt`, has been created at the root.

Terminal 1

Terminal

Loading...

Linux File System

Git and Git Version Control

Ask

[Introduction to text manipulation](https://www.educative.io/courses/web-application-penetration-testing/text-manipulation#Introduction-to-text-manipulation)

[Creating files and folders](https://www.educative.io/courses/web-application-penetration-testing/text-manipulation#Creating-files-and-folders)

[Removing files and folders](https://www.educative.io/courses/web-application-penetration-testing/text-manipulation#Removing-files-and-folders)

[Viewing and appending data to files](https://www.educative.io/courses/web-application-penetration-testing/text-manipulation#Viewing-and-appending-data-to-files)

[Vim editor](https://www.educative.io/courses/web-application-penetration-testing/text-manipulation#Vim-editor)