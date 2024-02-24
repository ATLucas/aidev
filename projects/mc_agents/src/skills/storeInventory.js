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
        console.log("INFO: No chest found within range.");
        return false;
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
            console.error(`ERROR: Failed to deposit ${item.name}: ${err.message}`);
            // Attempt to close the chest before exiting the function due to an error
            await chest.close();
            return false;
        }
    }

    // Close the chest after depositing items
    await chest.close();
    console.log("INFO: Chest closed.");

    return true;
}

module.exports = {
    storeInventory
};
