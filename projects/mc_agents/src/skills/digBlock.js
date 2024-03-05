// digBlock.js located in ./skills

async function digBlock(bot, block) {
    if (!bot.canDigBlock(block)) {
        console.log("INFO: Cannot dig this block:", block.name);
        return { success: false };
    }

    await new Promise((resolve, reject) => {
        // Start digging the block
        bot.dig(block, err => {
            if (err) {
                console.log("INFO: Failed to dig block:", block.name, err);
                reject(err);
            }
        });

        // Listen for the diggingCompleted event to resolve the promise
        bot.once('diggingCompleted', (completedBlock) => {
            if (completedBlock.position.equals(block.position)) {
                resolve();
            }
        });

        // Optionally, listen for a diggingAborted event to reject the promise
        bot.once('diggingAborted', (abortedBlock) => {
            if (abortedBlock.position.equals(block.position)) {
                reject(new Error(`Digging aborted: ${block.name}`));
            }
        });
    });

    return { success: true };
}

module.exports = {
    digBlock
};
