# TOM-Team-Thomais

Problem:
Finding a solution when presented with a problem that isn’t familiar to her
“Learning how to learn”


Strengths/what’s helpful:
list/steps
Interpreting visuals
Getting active feedback
Reading within reason (not too long of passages)
Creating art
Topics of interest (science, animals, titanic, urban legends)
Great memory recall within these topics
encouragement

Weaknesses:
Reading long passages
Finding steps to solve a problem


Goal:
Graphical interface product
How to identify the type of a problem
Set of algorithms/examples to help her solve a problem of that topic
Customizable - can add new topics as she learns more

Ideas:
Apple type interface
Easy to use web-app interface

Product Plan:
General menu
List of each type of problem
How to recognize
How to solve
Example
Pictures
Relatable objects to Thomais
Ability to create a new problem
Way to save all of the problems
Account?
An instance of the game solely distributed to Thomais

## Backend

### Database

The database is a json file in the structure of:


```javascript
"lessons":{
   "fractions":{
      "example":list<string>,
      "description":<string>,
      "additional_resources":list<string>,
      "image_url":string
   },
   "subtraction":{
         "example":list<string>,
         "description":<string>,
         "additional_resources":list<string>,
         "image_url":string
      }, ...
}
```


### API Endpoints

[GET] https://teamthomais.herokuapp.com/getGuideNames

Returns:

```json
[
  "Multiplication",
  "Subtraction",
  ...
]
```
