# 10k Day API

## What is 10k Day?
10k Day is a concept I crafted during the pandemic time for my home workouts.

It helps to track the amount of effort I put into my workouts to get the equivalent of 10 thousand steps made every day.

### Example:
I estimate that 10 push-ups is an equivalent of 400 steps. If I make 5x10 push-ups and 6k steps today, I will reach the 10k Day goal.

Everybody can set up their own exercises with their own estimations.

## Sample 10k Day interface

There is a simple app visualising the idea:
https://kornislaw.github.io/10k-day

Please note the example interface is entirely browser-based with no storage of progress (yet still useful for daily rutines - please see config examples at the bottom of the page). 
The intention of this project is to provide a backend for such interfaces.


## Installation

`poetry add fastapi`
`poetry add psycopg[binary]`

## Troubleshooting

* In case of issues with Poetry's cache at the moment it is best to just dump the whole cache from: `https://stackoverflow.com/questions/69326748/poetry-install-command-fails-whl-files-are-not-found#`
* 