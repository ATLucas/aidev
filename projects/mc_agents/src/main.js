const mineflayer = require('mineflayer');
const { pathfinder, Movements } = require('mineflayer-pathfinder');
const { BOT_CONFIG, START_POINT } = require('./config.js');
const { gatherResource } = require('./skills/gatherResource.js');


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

    if (message === 'gather wood') {
        console.log(`Received gather command from ${username}. Gathering wood...`);
        await gatherResource(bot, 'wood');
    }
});

bot.on('disconnect', (reason) => {
    console.log(`Disconnected: ${reason}`);
});

bot.on('error', (err) => {
    console.error('An error occurred:', err);
});