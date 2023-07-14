# Coding Standards
---
## Table of Contents

1. [Principals of When to Code](#principals-of-when-to-code)
2. [Global Scripts](#global-scripts)
3. [Custom Templates](#custom-templates)
4. [Custom Actions](#custom-actions)
5. [Tags](#tags)
6. [Linting](#linting)
7. [Pull Requests](#pull-requests)

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

While Custom Templates are a powerful tool to be leveraged while creating a custom user experience, it is important to remember that CPQ only supports it's Out-Of-The-Box functionality.  When SAP runs their updatates, you could find a template turned off, or erroring because of a change in system fields.  If custom work is the right path, there are some best practices to follow.

### 1. Templating out your code

- When we creat a custom version of a boilerplate CPQ template, we should attempt to leave that custom template as raw as possible.
- Instead, if we are adding 10+ lines of html, create a new template under, Shared - CustomScripts.
- Bracket your html and knockout.js in the below script tag.
```html
<script type="text/html" id="NameOfCustomTemplate">

    <!-- insert your code here -->
</script>
``` 

```html
<!-- ko template: { name 'NameOfCustomTemplate', data: 'if you need to pass data'} --><!-- /ko -->
```

## Custom Actions

## Tags

## Linting

## Pull Requests