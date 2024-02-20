// harvestTree.js located in ./skills

const { findClosestTree } = require('./findClosestTree');
const { digBlock } = require('./digBlock');
const Vec3 = require('vec3');

async function harvestTree(bot) {
    const treeBase = await findClosestTree(bot);
    if (!treeBase) {
        console.log("No tree found within range.");
        return;
    }

    // Assuming tree blocks are vertically aligned for simplicity
    let currentBlockPosition = new Vec3(treeBase.x, treeBase.y, treeBase.z);
    while (true) {
        const block = bot.blockAt(currentBlockPosition);
        if (!block || !['oak_log', 'spruce_log', 'birch_log', 'jungle_log', 'acacia_log', 'dark_oak_log'].includes(block.name)) {
             // No more tree blocks in this vertical line
            break;
        }
        await digBlock(bot, block);
        currentBlockPosition = currentBlockPosition.offset(0, 1, 0); // Move up to the next block
    }
}

module.exports = {
    harvestTree
};
