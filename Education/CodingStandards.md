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

## Principals of When to Code 

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

## Naming Conventions


### Global Scripts

Style: Pascal Case

Example: NameOfScript


### Custom Tables

Style: All Caps and Underscore For Table and Column names.

Example: NAME_OF_TABLE


### JS and Python Functions, Methods, and Variables

Style: Camel Case

Example: nameOfFunction(), nameOfVariable


### User Types

Style: Capitalize with Spaces.

Example: 'My New User Type'


### Custom Fields, Custom Quote Item Fields, Quote Table, Quote Table Columns

Style: Capitalize and Underscore

Example: Name_Of_Object


## Global Scripts

### Modules
The module 
#### When to use it:
You want to flip the module switch on a Global Script when all of your functions are completely isolated from each other.  They become Static, not remembering any data passed to them in between calls.
- Additionally, a module can be used to create an ENum, or static list of assigned variables.  In this case, append the script name with '_ENum'

#### How it's referenced:
```Python
import MyModuleName as mod

mod.yourFunctionName()
```
### Class

#### When to use it:

#### How it's referenced:
```Python
from GlobalScriptName import ClassName

class_instance = ClassName() 
class_instance.yourMethodName()
```
### Script

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

## Custom Templates

While Custom Templates are a powerful tool to be leveraged while creating a custom user experience, it is important to remember that CPQ only supports it's Out-Of-The-Box functionality.  When SAP runs their updates, you could find a template turned off, or erroring because of a change in system fields.  If custom work is the right path, there are some best practices to follow.

### 1. Templating out your code

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

## Custom Actions
Because Custom Actions can contain code/scripts it creates a large amount of locations that a potentially buggy script could be hiding. For this reason, if your code will contain more than 5 lines, it is best to house your code in a global script, and pass it a reference to the quote, as necessary.

```Python
ScriptExecutor.ExecuteGlobal('GlobalScriptName', context.Quote)
```

## Tags

## Linting
Having the proper Linters installed ensures that the code base remains clean and consistent.  They will through visual errors, on save, when linting standards are not being followed.

Please instal both linters:
- Flake 8
- Pylint

To activate linters, restart VS code after installation.

## Spell Check
Spelling errors are easy to make, and can lead to hours of debugging.  Please instal the following spell checker extension:
- Code Spell Checker

## Pull Requests

## Repository Branching
- Whenever you have a Story, Bug, Task, etc that results in committing code to the repository, you must create a new Branch, and name it after the ticket assigned to you
- Append onto the branch name with a basic description of the ticket.
- Example: "Tenant-Build-CPQ-#89_Create-Top-Of-Page-Button"