const mineflayer = require('mineflayer');
const { pathfinder, Movements } = require('mineflayer-pathfinder');
const { BOT_CONFIG, START_POINT } = require('./config.js');
const { navigateTo } = require('./skills/navigateTo.js');

const bot = mineflayer.createBot(BOT_CONFIG);

bot.on('spawn', () => {
    console.log('Bot has spawned.');
    console.log(`Teleporting to x: ${START_POINT.x}, y: ${START_POINT.y}, z: ${START_POINT.z}`);

    bot.loadPlugin(pathfinder);
    
    const defaultMove = new Movements(bot, require('minecraft-data')(bot.version));
    bot.pathfinder.setMovements(defaultMove);
    
    // Sleep for ten seconds before teleporting
    setTimeout(() => {
        bot.chat(`/tp ${START_POINT.x} ${START_POINT.y} ${START_POINT.z}`);
        
        const targetLocation = { x: 100, y: 64, z: 50 };
        navigateTo(bot, targetLocation);
    }, 10000); // 10000 milliseconds = 10 seconds
});

bot.on('chat', (username, message) => {
    console.log(`${username}: ${message}`);
});

bot.on('disconnect', (reason) => {
    console.log(`Disconnected: ${reason}`);
});

bot.on('error', (err) => {
    console.error('An error occurred:', err);
});