# Hilt
Hilt is a very small, very early in development game engine for text adventures.
# Creating a game
To start, create a config file with the `.hilt` extention.
```
MapSize(5, 5)
GameTitle("Frog Cave")
Cursor(">")
NullText("Nothing Here!")
ExitKey(q)


ShowMap(True)
MapNullText(" % ")
MapPlayerText("[o]")
```
Here is a breakdown of what each of these do<br>
<ul>
  <li>MapSize - Initialises the width and height of your Map</li>
  <li>GameTitle - This is the title of your game</li>
  <li>Cursor - Is what appears to the left of your input and is the cursor for selecting things with prompts (Which we will get to later)</li>
  <li>NullText - This is what the game will display when your character moves to a blank tile.</li>
  <li>ExitKey - This is the key to exit the game</li>
  <li>ShowMap - True or False, this will decide whether you show the map to the player after every move</li>
  <li>MapNullText - What you display on the map in space of a blank tile</li>
  <li>MapPlayerText - What you display on the map to represent the player</li>
</ul>
But now, lets create stuff.<br>

```
MakePlayer(0, 0)

MakeRoom{
    ID = Cave
    Location = 2, 2
    Icon = "[#]"
}

MakeRoom{
    ID = Shop
    Location = 0, 1
    Icon = "[$]"
}

MakeRoom{
    ID = House
    Location = 3, 3
    Icon = "[^]"
}
```
`MakePlayer` is integral to actally creating a game, the location is specified and relates to the map. 0, 0 in this case.<br>
`MakeRoom` has 3 parameters, the ID, which is like the variable name, the location, which is where it is located on the map, and the icon which will represent it on the map<br>
This is what our config file looks like, lets save this as `config.hilt` for example.<br>
Now, we can make our main file<br>

## Making the main file
The main file is where all the magic happens, where you can actually make sequences take place. To start, we need to import our config file. Like this:<br>
```
@config.hilt
```
Using `@` followed by the config file is how you import it.<br>
Now we can get to writing<br>
```
@config.hilt

OnEntry.Cave{
    prompt(
        ID = CavePrompt
        Text = "You find yourself in a cave. What do you do?"
        Options = ["Explore", "Run Out", "Dance"]
        Return = ["You found nothing...", "Everyone laughed at you for being such a 'crybaby'.", "Everyone posted you dancing on Instagram Reels. You got bullied."]
    )

}
```
This is how you can create an event, using `OnEntry.` followed by the ID we set earlier, in this case using the `Cave` ID, will allow for actions to happen when the player enters the given area or "Room"<br>
In this case, we will show a prompt, with the ID `CavePrompt` and text to be displayed followed by options and a return value.<br>
The `Text` is what will be printed out before the prompt<br>
The `Options` are the possible options for the user to pick from.<br>
`Return` is a corresponding return output, It needs to line up with the choice, for example, if the user chooses `"Run Out"`, the game will output the corresponding index (in this case index 1), being `"Everyone laughed at you for being such a 'crybaby'."`<br>
In the example (which you can find in this repo, the main file looks like this:<br>
```
@config.hilt



OnEntry.Cave{
    prompt(
        ID = CavePrompt
        Text = "You find yourself in a cave. What do you do?"
        Options = ["Explore", "Run Out", "Dance"]
        Return = ["You found nothing...", "Everyone laughed at you for being such a 'crybaby'.", "Everyone posted you dancing on Instagram Reels. You got bullied."]
    )

}

OnEntry.Shop{
    prompt(
        ID = ShopEntry
        Text = "You entered the busy market, eger for wares."
        Options = ["Buy wares", "Vlog it", "Sell Wares"]
        Return = ["You bought a gram of sheckledust. Probably should throw that away.", "You vlogged it!", "No one wanted to buy your loose paperclips and keycaps."]
    )

}

OnEntry.House{
    prompt(
        ID = House
        Text = "You relax in your lovely home. What do you watch?"
        Options = ["Breaking Bad", "Twin Peaks", "Nothing"]
        Return = ["You enjoyed it. Solid 9/10", "Your life changed! 100/10", "You are lonely"]
    )
}
```
This is a full example, the config creates 3 rooms and the main file initialises actions to happen on entry.<br>

# Important
It is important to note ***THIS IS VERY EARLY STAGE*** and I plan on expanding it much much more, but wanted to get it up here.<br>
Thank you for reading though!
