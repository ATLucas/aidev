// gatherResource.js located in ./skills
const { navigateTo } = require('./navigateTo.js');

/**
 * Finds and gathers a specific type of resource.
 * @param {object} bot - The mineflayer bot instance.
 * @param {string} resourceType - The type of resource to gather, e.g., "wood".
 */
async function gatherResource(bot, resourceType) {
    try {
        const targetBlockTypes = getResourceBlockType(resourceType); // Get the block types or names
        if (!targetBlockTypes) {
            console.log(`Resource type ${resourceType} is not recognized.`);
            return;
        }

        const targetBlock = bot.findBlock({
            point: bot.entity.position,
            matching: (block) => targetBlockTypes.includes(block.name),
            maxDistance: 64, // Adjust based on testing and performance considerations
            count: 1,
        });        

        if (!targetBlock) {
            console.log(`No ${resourceType} found within search radius.`);
            return;
        }

        await navigateTo(bot, targetBlock.position);
        
        // New checks before digging
        if (isBotCloseEnough(bot, targetBlock) && hasBotStoppedMoving(bot) && !bot.isDigging) {
            bot.isDigging = true; // Set flag before starting to dig
            await bot.dig(targetBlock);
            bot.isDigging = false; // Reset flag after digging
            console.log(`Successfully gathered ${resourceType}.`);
        } else {
            console.log("Conditions not met for digging.");
        }
    } catch (error) {
        console.error(`Error gathering resource ${resourceType}:`, error);
    }
}

/**
 * Maps a resource type to the corresponding block types in Minecraft.
 * @param {string} resourceType - The type of resource, e.g., "wood".
 * @returns {number[]} An array of block type IDs corresponding to the resource type.
 */
function getResourceBlockType(resourceType) {
    // Example for Minecraft version 1.17 or later; update block IDs as necessary
    const resourceMapping = {
        wood: ['oak_log', 'spruce_log', 'birch_log', 'jungle_log', 'acacia_log', 'dark_oak_log'], // Add any new wood types here
    };

    return resourceMapping[resourceType] || null;
}

const isBotCloseEnough = (bot, targetBlock) => {
    // Example check for proximity; refine as needed based on actual dig range and bot's position
    return bot.entity.position.distanceTo(targetBlock.position) < 2; // Check if the bot is within 2 blocks of the target
};

const hasBotStoppedMoving = (bot) => {
    return bot.entity.velocity.squaredLength() === 0; // Check if the bot's velocity is zero
};


module.exports = { gatherResource };
