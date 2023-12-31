# Coding Standards
---
## Table of Contents

1. [Principals of When to Code](#1-principals-of-when-to-code)
2. [Naming Conventions](#2-naming-conventions)
3. [Global Scripts](#3-global-scripts)
4. [Custom Templates](#4-custom-templates)
5. [Custom Actions](#5-custom-actions)
6. [Products](#6-Products)
7. [Tags](#7-tags)
8. [Linting](#8-linting)
9. [Spell Check](#9-spell-check)
10. [Pull Requests](#10-pull-requests)
11. [Repository Branching](#11-repository-branching)
12. [Multi Line Code](#12-multi-line-code)
13. [Hard Coding](#13-hard-coding)
14. [Logging Your Code](#14-logging-your-code)

## 1. Principals of When to Code 

Scripting, in general, is less performant than tags. If there's something that can be done with a tag, use a tag. It may be easier to use a script, but tag parsing is orders of magnitude faster and many scripts can slow down load times significantly. When first approaching a project, look at CTX tags, TABLE tags, LIST tags, and other tags in the Formula Builder first to see if there's a tag which can perform the task you're looking for. 
 
If custom logic is required and a tag won't suffice, try to cut out as many unnecessary processes as possible. For loops are very common in CPQ, so removing unnecessary loops and utilizing Pythonic functionality to remove/reduce nested looping structures will help with this. Python is a very powerful language with a lot of incredibly useful features that can save time and processing cycles when used properly. Some things to look into are:
- enumerate
- zip
- cycle
- itertools
- List comprehensions  
These will all help with removing unnecessary looping and help make code more performant.
 
Make sure to watch out for excessive database querying; it's very common that any SQL statements done inside of a loop can also be done once outside of a loop using something like SqlHelper.GetList instead of SqlHelper.GetFirst.
 
It's also worth mentioning that Traces can add significant processing time to code, so after debugging is complete it's best to remove them (or reduce the number if it's still being developed actively).

## 2. Naming Conventions


### 2.1. Global Scripts

    Style: Pascal Case

    Example: NameOfScript


### 2.2. Custom Tables

    Style: All Caps and Underscore For Table and Column names.

    Example: NAME_OF_TABLE


### 2.3. JS and Python Functions, Methods, and Variables
Make sure to name all variables/functions/methods after their purpose and not arbitrary letters and numbers.  If functions have a paired purpose, make sure that this is represented in the naming:
```js
function createInfoPopover(){
    // some code
}
function cancelInfoPopover(){
    // some code
}
```

    Style: Camel Case

    Example: nameOfFunction(), nameOfVariable


### 2.4. User Types

    Style: Capitalize with Spaces.

    Example: 'My New User Type'


### 2.5. Custom Fields, Custom Quote Item Fields, Quote Table, Quote Table Columns

    Style: Capitalize and Underscore

    Example: Name_Of_Object


## 3. Global Scripts

- Scripts should start with this header
```Python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   
#   Name:
#   Type: Module/Class/Script/API/CustomAction
#   Author: 
#   Copyright: Aspire Digital
#   Purpose:
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```
- Methods/Functions should start with this header
```Python
"""
Description: 
Parameters: 
    - (type):
    - (type):
"""
```
### 3.1. Modules

#### When to use it:
You want to flip the module switch on a Global Script when all of your functions are completely isolated from each other.  They become Static, not remembering any data passed to them in between calls.
- Additionally, a module can be used to create an ENum, or static list of assigned variables.  In this case, append the script name with '_ENum'

#### How it's referenced:
```Python
import MyModuleName as mod

mod.yourFunctionName()
```
### 3.2. Class

#### When to use it:

#### How it's referenced:
```Python
from GlobalScriptName import ClassName

class_instance = ClassName() 
class_instance.yourMethodName()
```
### 3.3. Script

#### When to use it:
This kind of GlobalScripting is best used when the script serves one single purpose.  While this script may be broken out into multiple functions, those functions would serve the purpose of "private" functions, only called internally.  This script consumes parameters with the 'Param' variable.
```Python
param1 = Param.param1
param2 = Param.param2
```

#### Return data

You can return data out of the script using the Variable 'Return'
```Python

Return = responseVariable
```

#### How it's referenced:
```Python
## no import required

ScriptExecutor.ExecuteGlobal('GlobalScriptName', {'param1': 1, 'param2': 'second value'})
```



## 4. Custom Templates

While Custom Templates are a powerful tool to be leveraged while creating a custom user experience, it is important to remember that CPQ only supports it's Out-Of-The-Box functionality.  When SAP runs their updates, you could find a template turned off, or erroring because of a change in system fields.  If custom work is the right path, there are some best practices to follow.

### 4.1. Templating out your code

##### We Should
- When we create a custom version of a boilerplate CPQ template, we should attempt to leave that custom template as raw as possible.
- Instead, if we are adding 10+ lines of html, create a new template under, Shared - CustomScripts.
- Bracket your html and knockout.js in the below script tag.
```html
<script type="text/html" id="NameOfCustomTemplate">

    <!-- insert your code here -->

</script>
``` 
- Then, back in the boilerplate custom template, you insert this at the bottom of the page.
```knockout.JS
@Html.PartialCustomTemplate('NameOfCustomTemplate')
```
This will alow you to reference said template anywhere within the page.  Any additional js scripts or <style> tag added in side the custom template will also be loaded into the DOM on page load.
- You can then call the template using knockout comment notation
```knockout.JS
<!-- ko template: { name 'NameOfCustomTemplate', data: 'if you need to pass data'} --><!-- /ko -->
```
- You can also reference the template inside an element using a data bind.
```knockout.JS
<span data-bind="template: { name: 'NameOfCustomTemplate', data: 'if you need to pass data'} "></span>
```
- Now, when future efforts are made to debug code in the Browsers Inspector, the named templates will actually align with the Custom Template file name.
- Additionally, we keep the code base clean and easy to maneuver.

##### We should never:
- Develop on a global User Type.  Instead, clone it.
- Develop on a template currently attached to globally used User Types.  Instead, make a copy and attach it to your own 'cloned' User Type 
- Nest the code code for a template directly inside another template.  Instead, make that nested code into its own template and call it as described above.
- Add a lot of code (all in a row) to a custom :boiler plate" template.  Instead make it its own template and call it.

### 4.2. 

### 4.3. 

## 5. Custom Actions
Because Custom Actions can contain code/scripts, it creates a large amount of locations where a potentially buggy script could be hiding. For this reason, if your code will contain more than a single line, it is best to house your code in a global script, and pass it a reference to the quote, as necessary.

```Python
ScriptExecutor.ExecuteGlobal('GlobalScriptName', context.Quote)
```
[More Global Script Info](#3-global-scripts)

## 6. Products
Because Products can contain code/scripts, it creates a large amount of locations where a potentially buggy script could be hiding. For this reason, if your code will contain more than a single line, it is best to house your code in a global script, and pass it a reference to the Product, as necessary.

```Python
ScriptExecutor.ExecuteGlobal('GlobalScriptName', Product)
```
[More Global Script Info](#3-global-scripts)

## 7. Tags

Tags exist as a faster way to access and process data related to quotes and products. They are more limited in terms of functionality but are much more performant. If you have the option to use a tag instead of a script, use a tag.

### 7.1. Special Tags
There are three special tags: CTX, LIST, and TABLE tags. These three tags have extra features and serve different purposes from other tags:
- CTX tags consolidate many of the existing tags into a singular place, while also offering many new tags to pull information that previously couldn't be pulled. CTX tags have built in formatting options for strings and numbers and can access contents of a container.
- TABLE tags query and return the first result in a specified custom table. The tag uses HANA SQL, which is very similar to MySQL or PL/SQL, and queries follow the same format as both of those languages. This works for any custom table, including system custom tables.
- LIST tags operate the same as a TABLE tag, but will return all values retrieved instead of the first value. The values are divided by a | with no spaces.

### 7.2. Tag Deprecation
When using Tags, especially in Document Generation, use CTX tag whenever possible to avoid deprecations, inside of the C and Q Tags.  A full list of deprecated tags can be found on the SAP CPQ website.  
    ```
    <<Q_TAG(<*CTX( Quote.Customer(BillTo).Company)*>)>>  
    <<C_TAG(<*CTX(Quote.CurrentItem.Description)*>)>>
    ```

## 8. Linting
Having the proper Linters installed ensures that the code base remains clean and consistent.  They will through visual errors, on save, when linting standards are not being followed.

Please install both linters:
- Flake 8
- Pylint

To activate linters, restart VS code after installation.

## 9. Spell Check
Spelling errors are easy to make, and can lead to hours of debugging.  Please install the following spell checker extension:
- Code Spell Checker

## 10. Pull Requests
- Anyone reviewing code in PR's (Pull Requests), should ensure that all standards were abided by before approving the PR.

- Once a pull request has been merged, make sure and close any accidental duplicate pull requests. 

## 11. Repository Branching
- Whenever you have a Story, Bug, Task, etc that results in committing code to the repository, you must create a new Branch, and name it after the ticket assigned to you
- Append onto the branch name with a basic description of the ticket.
- Example: "Tenant-Build-CPQ-#89_Create-Top-Of-Page-Button"

## 12. Multi Line Code

### 12.1. Long Strings
- Instead of using new line characters  

<span><img src="/Education/media/images/redX.png" width="20" height="20"/></span>
```Python
myVar = "I like my new car\nbecause it comes with a color/I like. "
``` 
- Use a long string  

<Span><img src="/Education/media/images/greenCheckBox.png" width="20" height="20"/></span>
```Python
myVar = '''
    I like my new car
    because it comes with a color
    I like.''' 
```

### 12.2. Breaking code into multi lines

Out linting standards constrain line length to 80 Characters or less, here are some ways to maintain this.

 - You can break you code to the next line after a '('    

<span><img src="/Education/media/images/redX.png" width="20" height="20"/></span>
```Python
myVar = FirstFunction.SecondFunction("This is a long string")
```
<Span><img src="/Education/media/images/greenCheckBox.png" width="20" height="20"/></span>
```Python
myVar = FirstFunction.SecondFunction(
    "This is a long string"
)
```

- You can also break you line up directly before a '.' and adding a '\\'    

<span><img src="/Education/media/images/redX.png" width="20" height="20"/></span>
```Python
myVar = FirstFunction.SecondFunction("This is a long string")
```
<Span><img src="/Education/media/images/greenCheckBox.png" width="20" height="20"/></span>
```Python
myVar = FirstFunction \
    .SecondFunction("This is a long string")
```

## 13. Hard Coding
This is a non-starter, full stop.

- If we need to access data within our scripts, you have two options:  

    #### 1. Reference a Global Script Module used as an Enum. (This is a Module that contains only variables.)
    ```python
    firstVariable = "some value"
    secondVariable = "some other value"
    ```  
    #### 2. Better Option is to Store this Data in a custom table.

- Do not assign hard coded numbers or strings straight into your code. Instead assign those numbers/string to a variable at the top of the function/method or class.

## 14. Logging Your Code

The purpose of Logs lies in the ability to track our process through the code, success or failure.  To do this we have instituted a StandardLogging class This is the standard for logging in the tenant. 

### StandardLogging

#### Imported:
```python
from StandardLogging import StandardLogging as log
```
#### Definitions:
```python

@staticmethod
def start(script_name, msg=""):
    """
    To be called at the entrance to a module or class
    Args:
        script_name (str): name of script being called
        explanation (str): purpose of script
    """

@staticmethod
def info(script_name, msg):
    """
    Displays a formatted message to the logs
    Args:
        message (str): Custom message to display
    """

@staticmethod
def error(script_name, msg=""):
    '''
    To be called when there is a error
    case in the code.
    Args:
        customMessage (str): Display more info to the user
    '''

@staticmethod
def exception(script_name, msg=""):
    '''
    Method to be called directly under the
    'except' in a try/except block.
    Args:
        customMessage (str): Display more info to the user
    '''

@staticmethod
def table(script_name, query, response=""):
    '''
    Method to be called inside a script whenever a table is accessed.
    Args:
        query (str): query string
        response (str): response from the query
    '''

@staticmethod
def quote(script_name, quote, msg=""):
    '''
    Method to be called at the top of any
    script that adjusts or accesses a quote.
    Args:
        quote (context.Quote): reference to the quote
        msg (str): to include what is accessed / modified
    '''
```
#### Note: 
- error() should be used when there is a logical error, such as:
    ```python
    x = 1
    if x is not 2:
        log.error('ScriptName', 'Invalid x value')
    ``` 
- exception() should be used to handle exceptions as such:
    ```python
    try:
        raise Exception()
    except Exception:
        log.exception('ScriptName', 'Exception raised while trying to ...')
    ```
- table() should be called at the end of a table call.  Convert return to string and log.  There may be certain times where the return value is too large by necessity.  In this case, log 'Return Value Bypassed' 