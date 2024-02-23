// goNear.js located in ./skills

const { goals: { GoalNear } } = require('mineflayer-pathfinder');

async function goNear(bot, target) {
    await bot.pathfinder.goto(new GoalNear(target.x, target.y, target.z, 2));
    return true;
}

module.exports = {
    goNear
};
