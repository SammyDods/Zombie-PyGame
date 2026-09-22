# Zombinator - Zombie PyGame

A shooter/strategy zombie game using the PyGame python module

I adapted the sprite animation, movement, and bullets from http://programarcadegames.com/index.php
This website was where I learned most of my pygame, and I could not have built this project without it.

You're a space marine trying to survive never ending waves of zombies. As the waves progress the zombies gain more health and eventually zombie tanks will spawn. You can use WASD to move, and your mouse to shoot. By killing zombies you earn cash, which you can then use on either buying suit upgrades (for increased damage) or buildings (with various bonuses). The buildings include banks (providing passive cashflow) and walls (walls will stop zombies from advancing until the walls run out of hp and can be shot through).

Use q to interact with the various buildings, p to pause (volume controls and quit are in the pause menu).


### Play
https://sammydods.itch.io/zombinator

### Run (desktop)
```
pip install pygame numpy
python main.py
```

### Run in browser (pygbag / itch.io)
```
pip install pygbag pygame-ce numpy
python -m pygbag .
```
Then open http://localhost:8000 in your browser (first load can take a while).

### Audio credits
- **80s Space Mission Music** by [Tomentum+](https://freesound.org/people/Tomentum/) — https://freesound.org/s/723496/ — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (background music)
- **Zombie tries to talk** by [l4red0](https://freesound.org/people/l4red0/) — https://freesound.org/s/181374/ — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Retro video game sfx - Explode** by [OwlStorm](https://freesound.org/people/OwlStorm/) — https://freesound.org/s/404754/ — [CC0](https://creativecommons.org/publicdomain/zero/1.0/)
- **Button hover.wav** by [Fachii](https://freesound.org/people/Fachii/) — https://freesound.org/s/338229/ — [CC0](https://creativecommons.org/publicdomain/zero/1.0/)
- **Launching 1** by [AceOfSpadesProduc100](https://freesound.org/people/AceOfSpadesProduc100/) — https://freesound.org/s/334268/ — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
