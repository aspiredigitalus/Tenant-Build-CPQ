# Coding Standards
---
## Table of Contents

1. [Principals of When to Code](#principals-of-when-to-code)
2. [Naming Conventions](#naming-conventions)
3. [Global Scripts](#global-scripts)
4. [Custom Templates](#custom-templates)
5. [Custom Actions](#custom-actions)
6. [Tags](#tags)
7. [Linting](#linting)
8. [Spell Check](#spell-check)
9. [Pull Requests](#pull-requests)
10. [Repository Branching](#repository-branching)
11. [Multi Line Code](#mulit-line-code)

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

    Style: Camel Case

    Example: nameOfFunction(), nameOfVariable


### 2.4. User Types

    Style: Capitalize with Spaces.

    Example: 'My New User Type'


### 2.5. Custom Fields, Custom Quote Item Fields, Quote Table, Quote Table Columns

    Style: Capitalize and Underscore

    Example: Name_Of_Object


## 3. Global Scripts

### 3.1. Modules
The module 
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

#### How it's referenced:
```Python
## no import required

ScriptExecutor.ExecuteGlobal('GlobalScriptName', {'param1': 1, 'param2': 'second value'})
```

#### Return data

You can return data out of the script using the Variable 'Return'
```Python

Return = responseVariable
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
Because Custom Actions can contain code/scripts it creates a large amount of locations that a potentially buggy script could be hiding. For this reason, if your code will contain more than 5 lines, it is best to house your code in a global script, and pass it a reference to the quote, as necessary.

```Python
ScriptExecutor.ExecuteGlobal('GlobalScriptName', context.Quote)
```

## 6. Tags

Tags exist as a faster way to access and process data related to quotes and products. They are more limited in terms of functionality but are much more performant. If you have the option to use a tag instead of a script, use a tag.

### 6.1. Special Tags
There are three special tags: CTX, LIST, and TABLE tags. These three tags have extra features and serve different purposes from other tags:
- CTX tags consolidate many of the existing tags into a singular place, while also offering many new tags to pull information that previously couldn't be pulled. CTX tags have built in formatting options for strings and numbers and can access contents of a container.
- TABLE tags query and return the first result in a specified custom table. The tag uses HANA SQL, which is very similar to MySQL or PL/SQL, and queries follow the same format as both of those languages. This works for any custom table, including system custom tables.
- LIST tags operate the same as a TABLE tag, but will return all values retrieved instead of the first value. The values are divided by a | with no spaces.

### 6.2. Tag Deprecation
When using Tags, especially in Document Generation, use CTX tag whenever possible to avoid deprecations, inside of the C and Q Tags.  A full list of deprecated tags can be found on the SAP CPQ website.

## Linting
Having the proper Linters installed ensures that the code base remains clean and consistent.  They will through visual errors, on save, when linting standards are not being followed.

Please instal both linters:
- Flake 8
- Pylint

To activate linters, restart VS code after installation.

## 7. Spell Check
Spelling errors are easy to make, and can lead to hours of debugging.  Please instal the following spell checker extension:
- Code Spell Checker

## 8. Pull Requests
Anyone reviewing code in PR's (Pull Requests), should ensure that all standards were abided by before approving the PR.

## 9. Repository Branching
- Whenever you have a Story, Bug, Task, etc that results in committing code to the repository, you must create a new Branch, and name it after the ticket assigned to you
- Append onto the branch name with a basic description of the ticket.
- Example: "Tenant-Build-CPQ-#89_Create-Top-Of-Page-Button"

## 10. Multi Line Code

### 10.1. Long Strings
- Instead of using new line characters