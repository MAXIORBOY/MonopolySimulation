# Monopoly Simulation is a heat map for the (classic) Monopoly game.

## Method:
The simulation was done, using the Monte Carlo method.

## Implementation:
```MonopolySimulation.__init__(self, turns=100, games=1000000)```
* ```turns``` - (int) a number of turns in a single game. Must be greater or equal to 1. Default = 100.
* ```games``` - (int) a number of games in the simulation. Must be greater or equal to 1. Default = 1000000.

## Assumptions:
* Financial aspect of the game is not included.
* If the "virtual player" is send to the jail, he pays the fee at the beginning of the next turn.

## Sources:
* Community chest cards: https://monopoly.fandom.com/wiki/Community_Chest
* Chance cards: https://monopoly.fandom.com/wiki/Chance
* Monopoly board: https://monopoly.fandom.com/wiki/Monopoly#Board

## Launch:
* Launch the ```view_results``` method from the ```MonopolySimulation``` class, to see the results.

## Technology:
* ```Python``` 3.8
* ```matplotlib``` 3.3.2
* ```numpy``` 1.19.4

## Screenshot:
![MS screenshot](https://user-images.githubusercontent.com/71539614/99747573-1137b500-2adb-11eb-8a64-bf1b38e8e0f7.png)
