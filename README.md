## NAME
simmer - runs sequenced timers

## SYNOPSIS
`simmer [-p <PERIODS>] [-y|--cycles <int>] [-x <command>] [-f <command>] [-o <path>] [-c <path>] [-d] [-h|--help]`

## OPTIONS
`-p <PERIODS>`: list of space-separated times for each period of the timer, of the format `[1m 1h 1s]` 
`-y <int>`: number of cycles the sequenced timer will repeat, an integer.
`-x <command>`: a command simmer will execute with each change to a new period.
`-f <command>`: a command simmer will execute when all cycles have finished.
`-o <path>`: a path to a file where simmer will write the time remaining.
`-c <path>`: a path to a config file with more granular period and command instructions.
`-d`: prints the time remaining to the console (STDOUT.)
`-h`: displays help.
