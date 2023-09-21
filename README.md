## NAME
simmer - runs sequenced timers

## SYNOPSIS
`simmer [-p <PERIODS>] [-y|--cycles <int>] [-x <command>] [-f <command>] [-F <command>] [-o <path>] [-c <path>] [-ds] [-h|--help]`

## OPTIONS
`-p|--periods <PERIODS>`: list of space-separated times for each period of the timer.
    Format as "1s 1m 1h 1d", with all periods contained in one argument.

`-y|--cycles <int>`: number of cycles the sequenced timer will repeat, an integer.

`-x|--execute <command>`: a command simmer will execute with each finished period.
    Format as `"<foo> -b ar -f 'Foo Bar'"`, with all arguments contained within a single string.
    *See also `--execboth`.*

`-f|--finishcyc <command>`: a command simmer will execute with each finished cycle.
    Format as `-x`.
    *See also `--execboth`.*

`-b|--execboth <command>`: Overrides command replacement at the end of a cycle.
    The `-x` and `-f` flags' default behavior is that one overrides the other. At the end of a cycle,
    instead of executing both the commands, the `-f` flag is prioritized. The `-b` flag specifies that both commands should be run.

`-F|--finally <command>`: a command simmer will run at the end of all cycles.
    Format as `-x`.

`-o|--output <path>`: a path to a file where simmer will write the time remaining.*

`-c|--config <path>`: a path to a config file with more granular period and command instructions.*

`-s|--stats`: Prints statistics such as period number and cycle number to the console at the end of each period.

`-d|--display`: Prints the time remaining to the console (STDOUT.)

`-t|--cmdout`: Pipes the output of any commands executed to the console.

`-h|--help`: displays help.*

^* not yet implemented
