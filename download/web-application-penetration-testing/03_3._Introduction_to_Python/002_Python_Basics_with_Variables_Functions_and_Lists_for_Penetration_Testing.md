# Python_Basics_with_Variables_Functions_and_Lists_for_Penetration_Testing

Source: https://www.educative.io/courses/web-application-penetration-testing/variables-functions-and-lists

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Variables, Functions, and Lists

Understand how to use variables, create functions, and manipulate lists in Python to build modular, efficient scripts essential for web application penetration testing. This lesson introduces key programming concepts that help organize code and prepare learners for practical security testing tasks.

We'll cover the following...

- [Variables](https://www.educative.io/courses/web-application-penetration-testing/variables-functions-and-lists#Variables)
- [Functions](https://www.educative.io/courses/web-application-penetration-testing/variables-functions-and-lists#Functions)
- [Lists](https://www.educative.io/courses/web-application-penetration-testing/variables-functions-and-lists#Lists)

## Variables[#](https://www.educative.io/courses/web-application-penetration-testing/variables-functions-and-lists#Variables)

**Variables** are names given to a value so that when the same name is used in the program, it invokes the associated value. Simply put, when we tell a program that we have a variable called `Dollar`, and we assign a value of `50` to it, then whenever we use or refer to `Dollar`, we get the aforementioned value.

Variables point to the information or data stored in the memory location with a value, such as integers, lists, real numbers, strings, floating-point numbers, booleans, and many more. Variables can also have custom data types assigned to them.

By the way, we’ve already seen and interacted with variables back in the string manipulation script.

In programming, guidelines must be followed to ensure that code is readable and efficient. These include the following:

- Use consistent cases for variable names. For example, choose between `number_one`, `NUMBER_ONE`, or `numberOne`, and ensure that all the variables in our scripts follow the same format.
- We have to ensure that our naming system in the entire program is sensible. To store the name of a month, a variable with the name `month` makes more sense than using only the letter `m`.
- Capital letters should be used to declare constant or global variables—for example `PI` or `USERCOUNT`.
- We cannot begin a variable name with a number.
- Long variable names are discouraged. Instead, use comments (for example, the `#` that turns the code green and non-executable).

## Functions[#](https://www.educative.io/courses/web-application-penetration-testing/variables-functions-and-lists#Functions)

**Functions** are blocks of code that perform a particular action. They help divide our program into smaller, modular chunks thus making the overall code more organized and manageable.

Python is popular because of how many convenient built-in functions it provides. There are functions and methods from official libraries, and there are custom packages as well; it’s a vast expanse of codebases that aim to make the lives of developers easier. Before we get to making our own functions, let’s first check out some examples of built-in functions:

## Built-in Functions

|  |  |
| --- | --- |
| **Function** | **Description** |
| `print()` | This displays output to the CLI. |
| `exit()` | This exits a program. |
| `float()` | This returns a floating-point number. |
| `help()` | This displays guidance on a specified object. |
| `range()` | This returns a list of integers within two specified values. It's helpful when working with loops. |
| `int()` | This converts a string number value to an integer. |
| `len()` | This returns the number of elements in a list. |
| `max()` | This returns the maximum value from the argument. |
| `pop()` | This removes and returns the last value or given index value from a list. |

Since we’ve already interacted with a number of built-in functions in the string manipulation section, we can skip ahead to making our own function instead.

We have two brief examples of simple custom functions provided below.

Python 3.8

```
# Return input_string as all uppercase and all lowercase.

# Example input:

#   AbC

# Example outputs:

#   ABC, abc

#   (ABC, abc)

def all_cases(input_string, flag):

up_string = input_string.upper()

low_string = input_string.lower()

if flag:

return up_string, low_string

else:

return (up_string, low_string)

# Return the middlemost character from a string.

# Example input: Mushrooms Hunting

# Example out: s

def middle_char(input_string):

return input_string[len(input_string) // 2:len(input_string) // 2 + 1]

# Testing our functions.

up_string, low_string = all_cases('AbC', True)

tuple_uplow_strings = all_cases('AbC', False)

print(up_string, low_string, type(up_string))

print(tuple_uplow_strings, type(tuple_uplow_strings))

print(middle_char('Mushrooms Hunting'))
```

⋯

Examples of user-defined functions

## Lists[#](https://www.educative.io/courses/web-application-penetration-testing/variables-functions-and-lists#Lists)

Those with previous non-Python programming experience may be familiar with arrays. An **array** is used to store multiple objects or variables of the same type. The values stored in an array can be stored, retrieved, deleted, and worked with using its index. In Python, the array is essentially known as a **list**.

List indexes begin from zero. The first element in the array will be stored at index zero, the second element is at index one, and so on. We’ve already experienced indexing; just recall the earlier examples from string manipulation (in Python, strings can also be indexed).

We have a brief demonstration of what we can do with lists, as shown below.

Python 3.8

```
# This is a list.

foods = ['apple', 'chocolate cake', 'shrimp fried rice', 'chips']

# Operations like slicing and indexing can be performed with lists as well.

print(foods[1:3])

# Adding items to the list.

foods.append('banana') # At the right-end.

print(foods)

foods.insert(2, 'ice cream') # At the given position.

print(foods)

# Removing items from the list.

del foods[2] # From the given position.

print(foods)

foods.remove('apple') # Specific item.

print (foods)

food_item = foods.pop() # Remove and return last item.

print(foods, 'Removed item:', food_item)

# Sorting the list.

foods.sort() # What do you think the output of this sort will be?

print(foods)
```

⋯

A brief introduction to basic list manipulation

Python Basics

Control Flow

Ask

[Variables](https://www.educative.io/courses/web-application-penetration-testing/variables-functions-and-lists#Variables)

[Functions](https://www.educative.io/courses/web-application-penetration-testing/variables-functions-and-lists#Functions)

[Lists](https://www.educative.io/courses/web-application-penetration-testing/variables-functions-and-lists#Lists)