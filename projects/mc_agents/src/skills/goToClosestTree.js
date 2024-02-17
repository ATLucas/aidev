// goToClosestTree.js located in ./skills

const { findClosestTree } = require('./findClosestTree');
const { navigateTo } = require('./navigateTo');
const Vec3 = require('vec3');

async function goToClosestTree(bot) {
    const treePosition = await findClosestTree(bot);
    if (treePosition) {
        const direction = treePosition.minus(bot.entity.position).normalize().scale(-2);
        const stopPosition = treePosition.plus(direction);
        // Ensure the y-coordinate is not altered
        stopPosition.y = treePosition.y;
        await navigateTo(bot, stopPosition);
    } else {
        console.log("No tree found within range.");
    }
}

module.exports = {
    goToClosestTree
};
