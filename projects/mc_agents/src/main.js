// main.js located in ./

const mineflayer = require('mineflayer');
const { pathfinder, Movements } = require('mineflayer-pathfinder');
const { BOT_CONFIG, START_POINT } = require('./config.js');
const { skillFunctions } = require('./skills.js');
const { createGPTAssistant, deleteGPTAssistant, performGPTCommand } = require('./gpt.js');

const bot = mineflayer.createBot(BOT_CONFIG);

bot.on('spawn', () => {
    console.log(`@${bot.username} has spawned.`);
    console.log(`INFO: Teleporting to (x=${START_POINT.x}, y=${START_POINT.y}, z=${START_POINT.z})`);

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

    if (command.startsWith('/')) {
        await performCommand(bot, command);
    } else {
        const response = await performGPTCommand(bot, command);
        bot.chat(response);
    }
});

async function performCommand(bot, command) {
    if (command.startsWith('/gototree')) {

        await skillFunctions["goToClosestTree"](bot);

    } else if (command.startsWith('/harvesttree')) {

        await skillFunctions["harvestTree"](bot);

    } else if (command.startsWith('/create')) {

        if (!gptAssistant) {
            await createGPTAssistant(bot);
        }

    } else if (command.startsWith('/reset')) {

        if (bot.gptAssistant) {
            await deleteGPTAssistant(bot);
        }
        await createGPTAssistant(bot);

    } else if (command.startsWith('/delete')) {

        await deleteGPTAssistant(bot);

    } else {
        console.warn(`Unrecognized command: ${command}`);
    }
}