const mineflayer = require('mineflayer');
const { pathfinder, Movements } = require('mineflayer-pathfinder');
const { BOT_CONFIG, START_POINT } = require('./config.js');
const { goToClosestTree } = require('./skills/goToClosestTree.js');
const { harvestTree } = require('./skills/harvestTree.js');


const bot = mineflayer.createBot(BOT_CONFIG);

bot.on('spawn', () => {
    console.log(`@${bot.username} has spawned.`);
    console.log(`Teleporting to (x=${START_POINT.x}, y=${START_POINT.y}, z=${START_POINT.z})`);
    console.log(bot.username);

    bot.loadPlugin(pathfinder);
    
    const defaultMove = new Movements(bot, require('minecraft-data')(bot.version));
    bot.pathfinder.setMovements(defaultMove);

    // Teleport to the starting point
    bot.chat(`/tp ${START_POINT.x} ${START_POINT.y} ${START_POINT.z}`);
});

bot.on('chat', async (username, message) => {
    console.log(`@${username}: ${message}`);

    if (!message.toLowerCase().startsWith(`@${bot.username.toLowerCase()}`)) {
        return;
    }

    const regex = new RegExp(`^@${bot.username}`, 'i');
    const command = message.replace(regex, '').trim();
    console.log(`@${bot.username}: ${command}`);

    if (command.startsWith('gototree')) {
        await goToClosestTree(bot);
    } else if (command.startsWith('harvesttree')) {
        await harvestTree(bot);
    }
});