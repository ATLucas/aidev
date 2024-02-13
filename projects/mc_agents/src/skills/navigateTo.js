const { goals: { GoalBlock } } = require('mineflayer-pathfinder');

function navigateTo(bot, target) {
    bot.pathfinder.setGoal(new GoalBlock(target.x, target.y, target.z));
}

module.exports = {
    navigateTo
};