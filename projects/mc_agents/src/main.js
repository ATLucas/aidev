const mineflayer = require('mineflayer');
const { BOT_CONFIG, START_POINT } = require('./config.js');

const bot = mineflayer.createBot(BOT_CONFIG);

bot.on('spawn', () => {
    console.log('Bot has spawned.');
    
    // Sleep for ten seconds before teleporting
    setTimeout(() => {
        console.log(`Teleporting to x: ${START_POINT.x}, y: ${START_POINT.y}, z: ${START_POINT.z}`);
        bot.chat(`/tp ${START_POINT.x} ${START_POINT.y} ${START_POINT.z}`);
        // call function here
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
