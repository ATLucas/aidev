// skills.js located in ./

const { queryInventory } = require('./skills/inventory.js');
const { harvestTree } = require('./skills/harvestTree.js');

const skillFunctions = {
    queryInventory,
    harvestTree,
};

module.exports = {
    skillFunctions
};
