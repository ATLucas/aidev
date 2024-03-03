// harvestTree.js located in ./skills

const { digBlock } = require('./digBlock');
const { goNear } = require('./goNear');
const { goTo } = require('./goTo');
const { queryInventory } = require('./queryInventory');
const Vec3 = require('vec3');

const LOG_BLOCKS = ['oak_log', 'spruce_log', 'birch_log', 'jungle_log', 'acacia_log', 'dark_oak_log'];

async function harvestTree(bot) {

    // Find the closest tree
    const treeBase = await findClosestTree(bot);
    if (!treeBase) {
        console.log("INFO: No tree found within range.");
        return { success: true };
    }

    // Go to the tree
    await goNear(bot, treeBase);

    // Harvest the tree
    const droppedItems = [];
    await harvestAdjacentTreeBlocks(bot, droppedItems, treeBase);

    // Collect the dropped logs
    console.log("INFO: Collecting items")
    for (const item of droppedItems) {
        await goTo(bot, item.position);
    }
    console.log("INFO: Done collecting items")
    return { success: true, inventory: queryInventory(bot) };
}

async function findClosestTree(bot) {
    const treeBlocks = LOG_BLOCKS;
    const maxDistance = 64; // Maximum search radius for trees
    const block = bot.findBlock({
        point: bot.entity.position,
        matching: block => treeBlocks.includes(block.name),
        maxDistance: maxDistance,
        minCount: 1,
    });

    if (block) {
        // Return the base of the tree (assuming the lowest log block is the base)
        return new Vec3(block.position.x, block.position.y, block.position.z);
    } else {
        // Return null if no tree is found within the search radius
        return null;
    }
}

async function harvestAdjacentTreeBlocks(bot, droppedItems, position, visited = new Set()) {

    const directions = [];
    for (let dx = -1; dx <= 1; dx++) {
        for (let dy = -1; dy <= 1; dy++) {
            for (let dz = -1; dz <= 1; dz++) {
                directions.push(new Vec3(dx, dy, dz));
            }
        }
    }

    for (const direction of directions) {
        const newPos = position.clone().add(direction);
        const key = newPos.toString();

        if (!visited.has(key)) {
            visited.add(key);
            const block = bot.blockAt(newPos);
            if (block && LOG_BLOCKS.includes(block.name)) {
                //console.log(`DEBUG: Tree block found at: ${newPos}`);
                
                // Listen for item drop
                const itemDropCallback = (entity) => {
                    if (entity.position.distanceTo(block.position) <= 1) {
                        droppedItems.push(entity);
                    }
                };
                bot.on('itemDrop', itemDropCallback);

                // Dig the block
                await digBlock(bot, block);

                // Stop listening for item drop
                bot.removeListener('itemDrop', itemDropCallback)

                // Continue harvesting
                await harvestAdjacentTreeBlocks(bot, droppedItems, newPos, visited);
            }
        }
    }
}

module.exports = {
    harvestTree
};
