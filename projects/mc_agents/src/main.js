import mineflayer from 'mineflayer';
import { BOT_CONFIG, START_POINT } from './config.js';

const bot = mineflayer.createBot(BOT_CONFIG);

bot.on('spawn', () => {
    console.log('Bot has spawned.');
    bot.chat(`/tp ${START_POINT.x} ${START_POINT.y} ${START_POINT.z}`);
});

bot.on('chat', (username, message) => {
    console.log(`${username}: ${message}`);
});

bot.on('disconnect', (reason) => {
    console.log(`Disconnected: ${reason}`);
});

bot.on('error', err => {
    console.error('An error occurred:', err);
});