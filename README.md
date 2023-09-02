## NAME
simmer - runs sequenced timers

## SYNOPSIS
`simmer [-p <PERIODS>] [-y|--cycles <int>] [-x <command>] [-f <command>] [-o <path>] [-c <path>] [-d] [-h|--help]`

## OPTIONS
`-p|--periods <PERIODS>`: list of space-separated times for each period of the timer, of the format `[1m 1h 1s]` \n
`-y|--cycles <int>`: number of cycles the sequenced timer will repeat, an integer.* \n
`-x|--execute <command>`: a command simmer will execute with each change to a new period.* \n
`-f|--finished <command>`: a command simmer will execute when all cycles have finished.* \n
`-o|--output <path>`: a path to a file where simmer will write the time remaining.* \n
`-c|--config <path>`: a path to a config file with more granular period and command instructions.* \n
`-d|--display`: prints the time remaining to the console (STDOUT.) \n
`-h|--help`: displays help.* \n

^* not yet implemented
