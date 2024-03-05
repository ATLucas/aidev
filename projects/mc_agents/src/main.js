// main.js located in ./

const mineflayer = require('mineflayer');
const { pathfinder, Movements } = require('mineflayer-pathfinder');
const { BOT_CONFIG, START_POINT } = require('./config.js');
const { skillFunctions } = require('./skills.js');
const { createGPTAssistant, deleteGPTAssistant, performGPTCommand } = require('./gpt.js');

const botRegistry = {};

async function createBot(botConfig) {
    try {
        const bot = mineflayer.createBot(botConfig);

        bot.on('spawn', async () => {
            try {
                await onBotSpawn(bot);
            } catch (error) {
                await handleError(error);
            }
        });

        bot.on('chat', async (username, message) => {
            try {
                await onBotChat(bot, username, message);
            } catch (error) {
                await handleError(error);
            }
        });

        return bot;
    } catch (error) {
        await handleError(error);
    }
}

async function onBotSpawn(bot) {
    console.log(`@${bot.username} has spawned.`);

    // Create a GPT for this bot
    await createGPTAssistant(bot);

    // Pathfinder setup
    bot.loadPlugin(pathfinder);
    const defaultMove = new Movements(bot, require('minecraft-data')(bot.version));
    bot.pathfinder.setMovements(defaultMove);

    // Teleport to starting location
    console.log(`INFO: Teleporting to (x=${START_POINT.x}, y=${START_POINT.y}, z=${START_POINT.z})`);
    bot.chat(`/tp ${START_POINT.x} ${START_POINT.y} ${START_POINT.z}`);
}

async function onBotChat(bot, username, message) {

    // Only pay attention to messages directed at this bot
    if (!message.toLowerCase().startsWith(`@${bot.username.toLowerCase()}`)) {
        return;
    }

    console.log(`@${username}: ${message}`);

    // Remove the direct address
    const regex = new RegExp(`^@${bot.username}`, 'i');
    const command = message.replace(regex, '').trim();

    // Check for command strings
    if (command.startsWith('/')) {

        // Check for spawn command
        if (bot.username === BOT_CONFIG["username"] && command.startsWith("/spawn")) {
            const [_, botName] = command.split(' ');
            if (botRegistry[botName]) {
                console.log(`Bot ${botName} already exists.`);
                return;
            }
            const newBotConfig = { ...BOT_CONFIG, username: botName };
            botRegistry[botName] = await createBot(newBotConfig);
            return;
        }

        // Process some other command
        await performCommand(bot, command);
    } else {

        // Send command to GPT
        bot.chat("Thinking...");
        const response = await performGPTCommand(bot, command);
        bot.chat(response);
    }
}

async function performCommand(bot, command) {
    if (command.startsWith('/create')) {

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

    } else if (command.startsWith('/come')) {

        await skillFunctions["come"](bot);

    } else if (command.startsWith('/inventory')) {

        await skillFunctions["queryInventory"](bot);

    } else if (command.startsWith('/store')) {

        await skillFunctions["storeInventory"](bot);

    } else if (command.startsWith('/harvesttree')) {

        await skillFunctions["harvestTree"](bot);

    } else if (command.startsWith('/collectitems')) {

        const [_, itemName, ...rest] = command.split(" ");

        await skillFunctions["collectItems"](bot, itemName);

    } else {
        console.warn(`Unrecognized command: ${command}`);
    }
}

async function handleError(error) {
    console.error(`ERROR: ${error}`);
    await cleanupBots();
    console.log('INFO: Exiting');
    process.exit(1);
}

async function cleanupBots() {
    console.log('INFO: Deleting GPTs before exiting');

    const deletePromises = Object.keys(botRegistry).map(botName => deleteGPTAssistant(botRegistry[botName]));
    await Promise.all(deletePromises);

    console.log('INFO: Cleanup complete');
}

// Modify the SIGINT handler to call cleanupBots
process.on('SIGINT', async () => {
    await cleanupBots();
    console.log('INFO: Exiting');
    process.exit();
});

// Initialize the bot
(async () => {
    botRegistry[BOT_CONFIG["username"]] = await createBot(BOT_CONFIG);
})();