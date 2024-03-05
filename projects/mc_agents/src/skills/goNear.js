// goNear.js located in ./skills

const { goals: { GoalNear } } = require('mineflayer-pathfinder');

async function goNear(bot, target, range=2) {
    await bot.pathfinder.goto(new GoalNear(target.x, target.y, target.z, range));
    return { success: true };
}

module.exports = {
    goNear
};
