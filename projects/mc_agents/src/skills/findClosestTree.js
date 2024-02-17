// findClosestTree.js located in ./skills

const Vec3 = require('vec3');

async function findClosestTree(bot) {
    const treeBlocks = ['oak_log', 'spruce_log', 'birch_log', 'jungle_log', 'acacia_log', 'dark_oak_log'];
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

module.exports = {
    findClosestTree
};
