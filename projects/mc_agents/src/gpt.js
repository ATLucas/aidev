// gpt.js located in ./

const fs = require('fs');
const path = require('path');
const OpenAI = require('openai');
const { skillFunctions } = require('./skills.js');

const openai = new OpenAI();

async function createGPTAssistant(bot) {

    concole.log(`INFO: Creating GPT for ${bot.username}`);

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
    
    bot.gptAssistant = await openai.beta.assistants.create({
        name: bot.username,
        instructions: instructions,
        tools: toolsData["tools"],
        model: "gpt-4-turbo-preview"
    });
    bot.gptThread = await openai.beta.threads.create();
}

async function deleteGPTAssistant(bot) {
    concole.log(`INFO: Deleting GPT for ${bot.username}`);
    if (bot.gptAssistant) {
        await openai.beta.assistants.del(bot.gptAssistant.id);
        bot.gptAssistant = null;
    }
}

async function performGPTCommand(bot, command) {

    if (!bot.gptAssistant) {
        await createGPTAssistant(bot);
    }

    const userMessage = await openai.beta.threads.messages.create(
        bot.gptThread.id, { role: "user", content: command }
    );

    let run = await openai.beta.threads.runs.create(
        bot.gptThread.id, { assistant_id: bot.gptAssistant.id }
    );

    while(run.status != "completed") {
        await delay(1000);

        run = await openai.beta.threads.runs.retrieve(bot.gptThread.id, run.id);

        if (run.status == "requires_action") {
            const toolOutputs = await _handleToolCalls(
                bot, run.required_action.submit_tool_outputs.tool_calls
            );

            run = await openai.beta.threads.runs.submitToolOutputs(
                bot.gptThread.id, run.id, { tool_outputs: toolOutputs }
            );
        }
    }

    const threadMessages = await openai.beta.threads.messages.list(bot.gptThread.id, after=userMessage.id);
    return threadMessages.data[0].content[0].text.value;
}

async function _handleToolCalls(bot, toolCalls) {

    const toolOutputs = [];

    for (const call of toolCalls) {
        const funcName = call.function.name;
        const args = JSON.parse(call.function.arguments);
        if (!skillFunctions[funcName]) {
            console.error(`ERROR: Function ${funcName} not found.`);
            return toolOutputs;
        }
        console.log(`INFO: Calling ${funcName}(${JSON.stringify(args)})`);
        const result = await skillFunctions[funcName](bot, ...Object.values(args));
        console.log(`INFO: Result of ${funcName}() call: ${result}`);
        toolOutputs.push({tool_call_id: call.id, output: result});
    }

    return toolOutputs;
}

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

module.exports = {
    createGPTAssistant,
    deleteGPTAssistant,
    performGPTCommand,
};
