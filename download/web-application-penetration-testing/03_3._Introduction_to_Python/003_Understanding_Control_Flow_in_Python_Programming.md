# Understanding_Control_Flow_in_Python_Programming

Source: https://www.educative.io/courses/web-application-penetration-testing/control-flow

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Control Flow

Explore how to use Python control flow elements such as if, elif, and else statements, nested conditionals, and loops like while and for. Understand these tools to write scripts that handle multiple conditions and repetitive tasks, essential for automating web security assessments.

We'll cover the following...

- [Conditional statements](https://www.educative.io/courses/web-application-penetration-testing/control-flow#Conditional-statements)
  - [Nested if statements](https://www.educative.io/courses/web-application-penetration-testing/control-flow#Nested-if-statements)
- [Loops](https://www.educative.io/courses/web-application-penetration-testing/control-flow#Loops)
  - [The while loop](https://www.educative.io/courses/web-application-penetration-testing/control-flow#The-while-loop)
  - [The for loop](https://www.educative.io/courses/web-application-penetration-testing/control-flow#The-for-loop)

## Conditional statements[#](https://www.educative.io/courses/web-application-penetration-testing/control-flow#Conditional-statements)

Let’s first discuss **conditional statements**. These allow us to perform certain sets of actions in our script, depending on certain sets of other actions or flags.

For example, assume we’re making a script that takes a number from the user as input, and we want it to:

- Print `+` when the number is positive.
- Print `-` when the number is negative.
- Print `=` when the number is zero.

This can be achieved with the `if`, `elif`, and `else` statements, as shown below:

Python 3.8

Ace Editor

1

2

3

4

5

6

7

8

9

10

11

def number\_type(input\_number):

if input\_number > 0:

print('+')

elif input\_number < 0:

print('-')

else:

print('=')

number\_type(287)

number\_type(-123)

number\_type(0)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

⋯

Example of basic conditionals

Keep in mind that in a conditional block, the very first conditional is always an `if`. It can then proceed to have as many `elif` blocks as we want, but it can only have one `else` block. Unlike the `if` block, the `else` block is optional.

For a list of the operators that we can use with `if` statements, please refer to the table below:

## Comparison Operators

|  |  |
| --- | --- |
| Operator | Meaning |
| `==` | Equal to |
| `!=` | Not equal to |
| `<` | Less than |
| `>` | Greater than |
| `>=` | Greater than or equal to |
| `<=` | Less than or equal to |

We can also make use of the boolean operators `or`, `and`, and `not`. If this is your first time facing conditional statements in any language, we recommend that you try out all the operators mentioned above in the code playground before proceeding.

### Nested `if` statements[#](https://www.educative.io/courses/web-application-penetration-testing/control-flow#Nested-if-statements)

We can have `if` statements inside other `if` statements. This is called **nesting**. This is particularly helpful when we need fine-grained control flows or when we have to process a lot of different flags to achieve a particular outcome.

Let’s revisit our previous block of code to see how nesting works:

Python 3.8

```
def number_type(input_number):

if input_number > 0:

if input_number > 1000:

print('+ Large')

else:

print('+ Small')

elif input_number < 0:

if input_number < -10000:

print('- Very small')

elif input_number == -1000:

print ('- Still rather small')

else:

print('- Just right')

else:

print('=')

number_type(1150)

number_type(506)

number_type(-13456)

number_type(-1000)

number_type(-9999)
```

⋯

A brief look at how nested conditionals work

## Loops[#](https://www.educative.io/courses/web-application-penetration-testing/control-flow#Loops)

**Loops** form an integral part of programming. They are essential, especially in enhancing repetitive tasks, and they make our code more readable and concise. Loops, when combined with conditional statements, form the basic building blocks of programming. While they’re not efficient, we can do most tasks with basic loops and conditional statements.

### The `while` loop[#](https://www.educative.io/courses/web-application-penetration-testing/control-flow#The-while-loop)

The `while` loop is used to repeat tasks as long as an expression is `True`. The moment the expression resolves to `False`, the loop breaks, and the rest of the script follows. If need be, we can also manually break out of `while` loops with `break` and skip certain iterations with `continue`.

Let’s check the code below to see it in action:

Python 3.8

```
def loop_de_loop(numbers):

while True:

if len(numbers) == 0:

break

print('Please provide a number between 1 and 10.')

check = numbers.pop()

if check == 'a number between 1 and 10':

print("You're free!")

break

elif int(check) >= 1 and int(check) <= 10:

print('Good number. But try again.')

else:

print("Can't you read? Try again.")

# First try this.

loop_de_loop([12, 5, 67, 1000, 87, 4])

# Then uncomment and try this.

#loop_de_loop([12, 5, 67, 'a number between 1 and 10', 87, 4])
```

⋯

Checking how a while loop works

### The `for` loop[#](https://www.educative.io/courses/web-application-penetration-testing/control-flow#The-for-loop)

The `for` loop is used to iterate a sequence of objects in a program code. In Python, we can iterate over lists, strings, tuples, dictionaries, and even sets without much effort.

There are two main ways to use the `for` loop, as shown below:

Python 3.8

```
def fruit_loops(fruits):

print('Method 1:')

# We pick items iteratively from the list.

for fruit in fruits:

print(fruit)

print('Method 2:')

# We assign a range for the list of items and manually index through it.

# This is equivalent to fruits[0], fruits[1], and so on.

for i in range(0, len(fruits)):

print(fruits[i])

print('Extra:')

# We can also provide a stopping point and how many items to skip

# during a loop. Here we are going from 10 to 0 in steps of 2.

for i in range(10, -1, -2):

print(i)

fruit_loops(['apple', 'banana', 'orange', 'tomato', 'guava'])
```

⋯

We learn how to iterate through a list with for loops

Variables, Functions, and Lists

Python Scripting

Ask

[Conditional statements](https://www.educative.io/courses/web-application-penetration-testing/control-flow#Conditional-statements)

[Nested if statements](https://www.educative.io/courses/web-application-penetration-testing/control-flow#Nested-if-statements)

[Loops](https://www.educative.io/courses/web-application-penetration-testing/control-flow#Loops)

[The while loop](https://www.educative.io/courses/web-application-penetration-testing/control-flow#The-while-loop)

[The for loop](https://www.educative.io/courses/web-application-penetration-testing/control-flow#The-for-loop)