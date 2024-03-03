// goTo.js located in ./skills

const { goals: { GoalBlock } } = require('mineflayer-pathfinder');

async function goTo(bot, target) {
    await bot.pathfinder.goto(new GoalBlock(target.x, target.y, target.z));
    return true;
}

module.exports = {
    goTo
};
