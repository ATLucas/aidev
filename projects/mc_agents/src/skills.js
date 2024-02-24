// skills.js located in ./

const { queryInventory } = require('./skills/queryInventory.js');
const { storeInventory } = require('./skills/storeInventory.js');
const { harvestTree } = require('./skills/harvestTree.js');

const skillFunctions = {
    queryInventory,
    storeInventory,
    harvestTree,
};

module.exports = {
    skillFunctions
};
