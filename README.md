<link rel="stylesheet" type="text/css" media="all" href="assets/css/readme.css" />

# Character rush

## Styling tip!

This document has more intricate
<span class="em"> styling</span> 
when viewed in a previewer such as eg. VS Code. 

## Introduction

This is a Python-based memory game with matrix vibes. 

Click 
[here](https://character-rush-05511809a26b.herokuapp.com/)
to navigate to the deployed app

## Development process

When I started working on this project, I wanted to craft a game inside the Python terminal that could respond to user inputs in real time. I was able to match this vision, but unfortunately, I couldn't replicate the user experience in the deployed 'browser terminal'. I entertained the thought of rebuilding the 'browser terminal' myself, but after some consideration, I decided to avoid getting sidetracked on this project. Therefore, the development process consists of two parts. 

1. Developing a starting point for the first project idea.
2. Developing the current version of the project.

Luckily, I was able to reuse some previously written code and I didn't find it to be that decremental. I've also documented the first project further down in this document.

##### Project diagrams
The first step was to prepare myself with project diagrams. The process of crafting a 'map' to visually and logically prepare myself was very helpful. Even though I didn't end up following perfectly, it worked as a guiding hand. It helped me to stay on track with my project goals. Sometimes, I feel that it can be alluring to prioritize features that may only 'enhance' the project rather than finishing it. In these moments, I used the project diagrams to steer me in the right direction.

![A 'sketchy' diagram of the foreseen development process (current version)](assets/images/readme/development_process/current_version/diagram_project.png "Project diagram") |

![A 'sketchy' diagram of the foreseen development process (current version)](assets/images/readme/development_process/current_version/diagram_code.png "Project diagram") |

## First version

Now, let's explore the first version of this project! If you'd like to try it out in a normal Python terminal, feel free to download the Python file and run it locally in a terminal of your choice. Click 
[HERE](https://github.com/KevinBjarnemark/character-rush/blob/main/first_version.py)
to navigate to the source code. 

#### Rules/instructions

The goal is to leap over the moving characters.

1. Read the moving character.
2. Type it in on your keyboard.
3. Press enter to jump.

The stickman will jump only when the correct character is submitted. 

![First version of this project](assets/images/readme/development_process/first_version/gameplay.gif "Gameplay of a stickman jumping over moving characters")

#### Disclaimer!

This game shouldn't be viewed as a finished product, but rather a 'starting point' for a larger project. Many features have not been implemented and the code does not follow best practices in terms of performance, optimization, refactoring, etc.

#### Project Incentive

Being able to type efficiently on a keyboard is almost mandatory in today's age. Likely, the user who plays this game will soon realize that a higher score can be reached by avoiding looking at the keyboard. Thus, they will unwittingly develop the skill of typing more efficiently and naturally while having fun at the same time.

A more comprehensive and long-term goal would be to target not only people who want to learn how to type on a keyboard but also professionals who seek to sharpen their skills. Perhaps a game like this could be published as a library for developers who want to be stimulated while waiting for a command to finish. This may be a long shot, but imagine running 'npm install' and, while the packages install, the developer can practice their typing skills with the packages installing in the background, without leaving the terminal.

#### Development

##### Initial sketch
![A 'sketchy' diagram of the foreseen development process (initial)](assets/images/readme/development_process/first_version/project_diagram.png "Project diagram")

Most of the implemented concepts have already been explained in this document. One distinction though, is that the user input runs on its own thread. This is to prevent the terminal from pausing the script when the user has to submit a character in order to jump.

#### Features to be implemented

If you want to further develop this project, here are some suggestions of what you might want to implement.

<details>
    <summary>
        Speed control
    </summary>

The user should be able to dial in the speed of the moving characters
</details>

<details>
    <summary>
        Gameplay
    </summary>

Right now, if the user jumps too late, the characters will run through the legs, causing a glitchy effect. There's no real need to fix this if a game reset occurs at that point. However, it may be wise to fix this if, for example, a 'practice mode' gets implemented. Perhaps creatively, by making the stickman fall or something similar.
</details>

<details>
    <summary>
        Game modes
    </summary>

- Increase the speed for every successful jump.
- Adjust difficulty
</details>

<details>
    <summary>
        More
    </summary>

- Scoring system and scoreboard.
- Let the user input custom characters/symbols
- Add a skateboard
</details>

## Code

### #1
##### How frames are printed

The game is based on the concept of FPS (frames per second). The speed variable controls the rate at which the frames are printed and is set to 0.1 by default. To print the frames, I decided to use the built-in Python package 'sys'. This package enables control over the cursor, allowing drawing in the terminal without printing new lines. It's similar to drawing an image, clearing the canvas, and quickly redrawing a new image. To demonstrate this, watch the flashing cursor in action in any of the gameplay videos above.

This approach allows us to first, draw the frames conditionally, and then render those frames on a line-by-line basis.

### #2
##### How y is calculated

Imagine our 'printing press' just starting up (with an infinite amount of paper) and the task is to print the 'current frame'. The only part of the frame that is changing is the raining characters, so we need to surgically insert them in the correct row (y) per frame. The amount of characters can vary so we'll read them top-down, insert them in a falling matter, then delete the top-most character as soon as the character at hand is out of bounds. In this way, it'll be the same 'rap' in the next iteration. 

1. Read the characters top-down
2. Insert character (i) in the correct row (y)
3. Delete the top-most character (when it is out of bounds)

To insert the characters, the printing press would look at the distance to the ground (rows) and subtract it from the character index (i). In practice, the printing press will be prepared to read eg. 5 rows. Then it subtracts 5 by the character index eg. 5, giving us 0. This makes sense because the fifth character should be placed at the top since it is the last character falling down. 

It gets a bit more complicated in the first couple of frames. Before the first characters have reached the ground, we'll need to 'push' them incrementally. To exemplify this, if frame_count = 1 and i = 0 y will be **(1 - 1 - 0)** placing it at the top. The next frame y  will be **(2 - 1 - 0)**, placing it on the second row. In other words, the frame_count will push the characters down with each frame. As soon as the frames surpass the number of rows, we don't need to push the characters anymore.

By the time a character moves out of bounds, the top-most character in the list will be removed, ensuring the rain effect continues seamlessly. 

## Credits

##### Template
To get the Python console into the browser I used template files provided by Code Institute 
[Source](https://github.com/Code-Institute-Solutions/love-sandwiches-p5-sourcecode/tree/master/05-deployment/01-deployment-part-1)

##### External sources

For manipulating the terminal (moving the cursor, changing colors, etc.) I've been using this cheatsheet by [ConnerWill](https://gist.github.com/ConnerWill) on GitHub
[Source](https://gist.github.com/ConnerWill/d4b6c776b509add763e17f9f113fd25b)

## Third-parties

##### [Third party libraries](https://github.com/KevinBjarnemark/character-rush/blob/main/package.json)
These packages are listed in the package.json file and requirements.txt

##### [Excalidraw](https://excalidraw.com/)

Excalidraw is an online drawing tool that I used for drawing the development diagram.
