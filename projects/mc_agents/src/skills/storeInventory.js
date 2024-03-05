// storeInventory.js located in ./skills

const { goNear } = require('./goNear');
const Vec3 = require('vec3');

async function storeInventory(bot) {
    // Find the nearest chest within a specified radius
    const chestBlock = bot.findBlock({
        point: bot.entity.position,
        matching: block => block.name === 'chest',
        maxDistance: 64,
        minCount: 1,
    });

    if (!chestBlock) {
        const errMsg = "No chest found within range.";
        console.log(`INFO: ${errMsg}`);
        return {success: false, error: errMsg};
    }

    // Convert the chest block position to Vec3 for goNear
    const chestPosition = new Vec3(chestBlock.position.x, chestBlock.position.y, chestBlock.position.z);

    // Go near the chest
    await goNear(bot, chestPosition);

    // Open the chest
    const chest = await bot.openChest(chestBlock);
    console.log("INFO: Chest opened.");

    // Deposit each inventory item into the chest
    for (const item of bot.inventory.items()) {
        try {
            await chest.deposit(item.type, null, item.count);
            console.log(`INFO: Deposited ${item.count} of ${item.name}.`);
        } catch (err) {
            // Attempt to close the chest before exiting the function due to an error
            await chest.close();

            const errMsg = `Failed to deposit ${item.name}: ${err.message}`;
            console.error(`ERROR: ${errMsg}`);
            return {success: false, error: errMsg};
        }
    }

    // Read the chest contents after depositing items
    const chestContents = {};
    chest.containerItems().forEach(item => {
        if (chestContents[item.name]) {
            chestContents[item.name] += item.count;
        } else {
            chestContents[item.name] = item.count;
        }
    });

    // Close the chest after depositing items
    await chest.close();
    console.log("INFO: Chest closed.");

    return { success: true, chestContents: chestContents };
}

module.exports = {
    storeInventory
};
