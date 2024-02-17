const mineflayer = require('mineflayer');
const { pathfinder, Movements } = require('mineflayer-pathfinder');
const { BOT_CONFIG, START_POINT } = require('./config.js');
const { navigateTo } = require('./skills/navigateTo.js');
const { findClosestTree } = require('./skills/findClosestTree.js');
const { goToClosestTree } = require('./skills/goToClosestTree.js');


const bot = mineflayer.createBot(BOT_CONFIG);

bot.on('spawn', () => {
    console.log('Bot has spawned.');
    console.log(`Teleporting to x: ${START_POINT.x}, y: ${START_POINT.y}, z: ${START_POINT.z}`);

    bot.loadPlugin(pathfinder);
    
    const defaultMove = new Movements(bot, require('minecraft-data')(bot.version));
    bot.pathfinder.setMovements(defaultMove);

    // Teleport to the starting point
    bot.chat(`/tp ${START_POINT.x} ${START_POINT.y} ${START_POINT.z}`);
});

bot.on('chat', async (username, message) => {
    console.log(`${username}: ${message}`);

    if (message.startsWith('navigate')) {
        const args = message.split(' '); // Split the message into parts
        if (args.length === 4) { // Check if there are exactly 4 parts: "navigate" and the three coordinates
            try {
                const x = parseFloat(args[1]);
                const y = parseFloat(args[2]);
                const z = parseFloat(args[3]);
                const target = { x, y, z }; // Create a Vec3 object for the target location
                await navigateTo(bot, target);
            } catch (error) {
                console.error('Error parsing coordinates:', error);
            }
        } else {
            bot.chat("Usage: navigate <x> <y> <z>");
        }
    }

    if (message.startsWith('findtree')) {
        const closestTreePos = await findClosestTree(bot);
        console.log(closestTreePos);
    }

    if (message.startsWith('gototree')) {
        await goToClosestTree(bot);
    }
});

bot.on('disconnect', (reason) => {
    console.log(`Disconnected: ${reason}`);
});

bot.on('error', (err) => {
    console.error('An error occurred:', err);
});