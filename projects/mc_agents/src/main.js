const mineflayer = require('mineflayer');
const { pathfinder, Movements } = require('mineflayer-pathfinder');
const { BOT_CONFIG, START_POINT } = require('./config.js');
const { goToClosestTree } = require('./skills/goToClosestTree.js');
const { harvestTree } = require('./skills/harvestTree.js');
const fs = require('fs');
const path = require('path');

const OpenAI = require('openai');
const openai = new OpenAI();

const bot = mineflayer.createBot(BOT_CONFIG);
let gptAssistant = null;
let gptThread = null;

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
        if (command.startsWith('/gototree')) {
            await goToClosestTree(bot);
        } else if (command.startsWith('/harvesttree')) {
            await harvestTree(bot);
        } else if (command.startsWith('/create')) {
            if (!gptAssistant) {
                await createGPTAssistant();
            }
        } else if (command.startsWith('/reset')) {
            if (gptAssistant) {
                await deleteGPTAssistant();
            }
            await createGPTAssistant();
        } else if (command.startsWith('/delete')) {
            await deleteGPTAssistant();
        } else {
            console.warn(`Unrecognized command: ${command}`);
        }
    } else {
        const response = await performGPTCommand(command);
        bot.chat(response);
    }
});

// TODO: Move the rest to a different file

async function createGPTAssistant() {

    const instrPath = path.join(__dirname, 'gpt/instructions.md');
    const toolsPath = path.join(__dirname, 'gpt/tools.json');

    let instructions;
    let toolsData;
    
    try {
        instructions = fs.readFileSync(instrPath, 'utf8');
        const rawToolsData = fs.readFileSync(toolsPath, 'utf8');
        toolsData = JSON.parse(rawToolsData);
    } catch (error) {
        console.error('Error reading files:', error);
        return null;
    }
    
    gptAssistant = await openai.beta.assistants.create({
        name: bot.username,
        instructions: instructions,
        tools: toolsData["tools"],
        model: "gpt-4-turbo-preview"
    });
    gptThread = await openai.beta.threads.create();
}

async function deleteGPTAssistant() {
    if (gptAssistant) {
        await openai.beta.assistants.del(gptAssistant.id);
        gptAssistant = null;
    }
}

async function performGPTCommand(command) {

    if (!gptAssistant) {
        await createGPTAssistant();
    }

    const userMessage = await openai.beta.threads.messages.create(
        gptThread.id, { role: "user", content: command }
    );

    let run = await openai.beta.threads.runs.create(
        gptThread.id, { assistant_id: gptAssistant.id }
    );

    while(run.status != "completed") {
        await delay(1000);

        run = await openai.beta.threads.runs.retrieve(gptThread.id, run.id);

        if (run.status == "requires_action") {
            const toolOutputs = await handleToolCalls(
                run.required_action.submit_tool_outputs.tool_calls
            );

            run = await openai.beta.threads.runs.submitToolOutputs(
                gptThread.id, run.id, { tool_outputs: toolOutputs }
            );
        }
    }

    const threadMessages = await openai.beta.threads.messages.list(gptThread.id, after=userMessage.id);
    return threadMessages.data[0].content[0].text.value;
}

const functionMap = {
    goToClosestTree,
    harvestTree
};

async function handleToolCalls(toolCalls) {

    const toolOutputs = [];

    for (const call of toolCalls) {
        const funcName = call.function.name;
        const args = JSON.parse(call.function.arguments);
        if (functionMap[funcName]) {
            console.log(`INFO: Calling ${funcName}(${JSON.stringify(args)})`);
            const result = await functionMap[funcName](bot, ...Object.values(args));
            console.log(`INFO: Result of ${funcName}() call: ${result}`);
            toolOutputs.push({tool_call_id: call.id, output: result});
        } else {
            console.error(`ERROR: Function ${funcName} not found.`);
        }
    }

    return toolOutputs;
}

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));