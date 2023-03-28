# Sproutland Valley
I'm currently learning Python through [Exercism](https://exercism.org/), but I've wanted to try out a few of the concepts in real project. Since I love computer games, and I LOVE Stardew Valley, using [Clear Code's](https://www.youtube.com/@ClearCode) tutorial, *Creating a Stardew Valley Inspired Game in Python*, seemed like a great chance to try a few things out.

## What did I learn?

#### **Delta time (dt)**
Delta time is the difference between the current and previous frame. You can multiply any movement in the game by this number to make it run smoothly at any frame rate. Movement * Frame Rate * Delta Time = Apparent Movement

|**Frames/Second**|**Pixels/Frame** |**Delta**        |**Pixels/Second**|
|-----------------|-----------------|-----------------|-----------------|
| 10              | 10              | 1/10 = 0.1      | 10              |     
| 30              | 10              | 1/30 = 0.33     | 10              |
| 60              | 10              | 1/60 = 0.17     | 10              |
| 120             | 10              | 1/120 = 0.08    | 10              |
| 600             | 10              | 1/600 = 0.002   | 10              |

If used, *anything* which moves in the game will need delta time applied; animations, rotations, movements, etc. It also means larger numbers are involved (10 pixels / second is really slow, for example). But be careful, delta movements are floating point numbers and Pygame needs *integers* for placing rects because it's pixel information (no such thing as half a pixel). If you only store the position inside the rect, high frame rates can mean no movement as the rect truncates the floating point delta (to 0), so storing the position inside a unique variable is necessary.

#### **Normalising a Vector**
When considering player movement, if they press 2 keys at the same time (i.e. up and right), they will move faster than in just one direction (Pythagoras a^2 + b^2 = c^2). Pygame has an inbuilt method for doing this!

## Resources
### Documention and Guides
- [Pygame Docs](https://www.pygame.org/docs/)
- [Creating a Stardew Valley inspired game in Python](https://www.youtube.com/watch?v=T4IX36sP_0c)

### Assets
- **Art:** [Sprout Lands Asset Pack](https://cupnooble.itch.io/sprout-lands-asset-pack) by [Cup Nooble](https://cupnooble.itch.io/).
- **Sound Effects:** 
- **Music**: 

### Other Programs
- [Tiled](https://www.mapeditor.org/) - An open source, fully-featured level editor