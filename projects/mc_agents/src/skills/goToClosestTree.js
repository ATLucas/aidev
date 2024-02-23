// goToClosestTree.js located in ./skills

const { findClosestTree } = require('./findClosestTree');
const { goNear } = require('./goNear');
const Vec3 = require('vec3');

async function goToClosestTree(bot) {
    const treePosition = await findClosestTree(bot);
    if (treePosition) {
        await goNear(bot, treePosition);
        return true;
    } else {
        console.log("No tree found within range.");
        return false;
    }
}

module.exports = {
    goToClosestTree
};
