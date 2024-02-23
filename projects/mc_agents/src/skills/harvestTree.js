// harvestTree.js located in ./skills

const { findClosestTree } = require('./findClosestTree');
const { digBlock } = require('./digBlock');
const Vec3 = require('vec3');

async function harvestAdjacentTreeBlocks(bot, position, visited = new Set()) {
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
            if (block && ['oak_log', 'spruce_log', 'birch_log', 'jungle_log', 'acacia_log', 'dark_oak_log'].includes(block.name)) {
                console.log(`Tree block found at: ${newPos}`);
                await digBlock(bot, block);
                await harvestAdjacentTreeBlocks(bot, newPos, visited);
            }
        }
    }
}

async function harvestTree(bot) {
    const treeBase = await findClosestTree(bot);
    if (!treeBase) {
        console.log("No tree found within range.");
        return false;
    }
    await harvestAdjacentTreeBlocks(bot, treeBase);
    return true;
}

module.exports = {
    harvestTree
};
