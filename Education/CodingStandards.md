# Coding Standards
---
## Table of Contents

1. [Principals of When to Code](#principals-of-when-to-code)
2. [Global Scripts](#global-scripts)
3. [Custom Templates](#custom-templates)
4. [Custom Actions](#custom-actions)
5. [Tags](#tags)
6. [Linting](#linting)
7. [Spell Check](#spell-check)
8. [Pull Requests](#pull-requests)

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

## Global Scripts

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
- Then, back in the boilerplate custom tempalte, you insert this at the bottom of the page.
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

## Tags

## Linting
Having the proper Linters installed ensures that the code base remains clean and consistent.  They will through visual errors, on save, when linting standards are not being followed.

Please instal both linters:
- Flake 8
- Pylint

## Spell Check
Spelling errors are easy to make, and can lead to hours of debugging.  Please instal the following spell checker extension:
- Code Spell Checker

To activate linters, restart VS code after installation.

## Pull Requests