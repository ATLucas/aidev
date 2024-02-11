# Minecraft Agents

The following guide assumes you are running on a Mac, but most instructions can easily be tweaked for other platforms.

## Minecraft Server Setup

1. Download Minecraft launcher
2. Start the launcher and sign-in with your Microsoft account
3. Buy Java Edition
4. Create a version 1.20.1 installation for Mineflayer compatibility
    - Select the "Installations" tab
    - Click "New installation" button
    - Name it "Minecraft 1.20.1"
    - Select version "1.20.1"
    - Leave other options as defaults
    - Click "Create" button at bottom right
5. Return to the "Play" tab
6. Select "Minecraft 1.20.1" in the drop-down at the bottom left of the center modal
7. Click "PLAY"
8. Click "Singleplayer"
9. Create a new world:
    - Allow cheats so that you can teleport your bot
    - I'm currently using seed 222
    - Start with a "peaceful" world
10. Start the world
11. Make your server available on your LAN network:
    - Press `ESCAPE` -> Options -> Open to LAN
    - `Game Mode`: `Survival`
    - `Allow Cheats`: `ON`
    - `Port Number`: `3001`
    - Click "Start LAN World"

## MC Agents Setup

1. Go to the [Node.js official website](https://nodejs.org/en).
2. Download the "LTS" version
3. Run the installer
4. Verify installation by running `node -v`

## Run MC Agents

1. `cd aidev/projects/mc_agents/src`
2. `node main.js`

## Tips

- Show debug info: `FN` + `F3`
- Set the world to daytime:
    - Press `T`
    - Type "/time set day"
    - Press `ENTER`