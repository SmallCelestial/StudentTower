# StudentTower 
![Pygame logo](docs/pygame_powered.png)  

## Credits
- First Contributor [SmallCelestial](https://github.com/SmallCelestial)  
- Second Contributor [ppaczek04](https://github.com/ppaczek04)
  
## What our game is about
StudentTower was inspired by old yet still legendary game **Icy Tower**. 
The main character "Bob" is placed in a never ending tower which as time passes starts to collapse from the bottom!
The goal of a player is to help Bob get as high as possible, the higher you go the better score you get. Jumping with style makes you earn additional points, so called combos. But be careful, after some time steps start to collapse, so you have to hurry!

## Requirements
Our game is based on **pygame** library.  
```
pip install pygame
```
## Project structure:
Files metioned below contain classes (and their descriptions) responsible for game functionality:
- main.py
- engine.py
- player.py
- steps_lib.py
- screens.py
## Tests:
Our projects include tests written in **Unittest** and **pytest** frameworks. You can find them in _test_ dictionary. Each file has specific name indicating for which class tests it include.
## Database:
We decided to implement database based on **SQLite3** framework. It collects data about best score player has got, and it shown after player either dies.

## License 
No license was included for this project, We reserve the right to place future versions of this library under some specific license.
 
