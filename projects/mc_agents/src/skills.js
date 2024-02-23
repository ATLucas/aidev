// skills.js located in ./

const { goToClosestTree } = require('./skills/goToClosestTree.js');
const { harvestTree } = require('./skills/harvestTree.js');

const skillFunctions = {
    goToClosestTree,
    harvestTree
};

module.exports = {
    skillFunctions
};
