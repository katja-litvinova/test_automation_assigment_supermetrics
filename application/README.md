# Supermetrics Test Automation Assessment

## Introduction

This repo contains the code for an exciting new product, Supermetrics Kitty Manager. Unfortunately, it has been built without any tests at all and may contain serious production bugs.

It is your task to spend 2-3 hours setting up what you consider to be the most important tests for this codebase. You should be prepared to discuss your decisions in an interview, and also to be able to elaborate on how you would continue testing this app if you had more time. We are primarily looking for evidence of your skills in building and managing automated tests with this assignment, but you may consider manual testing as an additional part of your strategy.

You should feel free to alter the code to make it more testable, but we will not evaluate you on the quality of any changes you may make. As this code was built without tests it may well contain real bugs - in which case feel free to fix them.

Note that the code in this repository is not indicative of the standard quality of Supermetrics code, it was created for assignment purposes only.

## Submitting the task

Copy this code to a new repository to work in. Please send us a link to a publicly-accessibly repository with the changes. You do not need to use GitHub. Do not make a pull request to this repository, and do not send us a zipped repository.

## Running the test app

This is a relatively simple Next.js app written in TypeScript. To run it you should,

1. Install dependencies with `yarn`
2. Start the dev server with `yarn dev`

API routes have been used to simulate the presence of a backend, the code there is not even close to production-ready but should suffice for this task.

There is a small degree of persistence in the app data. To reset the app data you can do one of the following,

-   GET `localhost:3000/api/reset`
-   Click the `Reset` button in the top-right of the running app

The valid login credentials for the app are,

1. Username: "admin", password: "adminpass" for admin user
2. Username: 'user', password: "helloworld" for normal user

## Functional requirements

To help you plan your tests, here are some functional requirements for the app,

1.  Users can log in by providing a user name and password
2.  When not logged-in, only the login page can be visited by a user
3.  Logged-in users are categorised as "normal users" or "admin users"
4.  All logged-in users are able to see a list of cats on the home page
    1. This list includes a name, picture, awesomeness rating and rank (in order of descending awesomeness) for each cat
    2. Awesomeness is calculated as the sum of the ASCII character codes for the letters of the cat's name (cats only user ASCII characters in their names). However if the cat's name is exactly "James", the awesomeness is infinite.
    3. The cats are presented in descending order of awesomeness.
5.  Only admin users are able to delete cats from the list.
6.  All logged-in users may rename cats but 2 cats may never share a name (cats are not picky about their exact names but desire to feel unique)
7.  Any changes to the cat list are persisted between visits to the app.

## Attribution

All cat images are used without modification from https://placekitten.com/attribution.html.
