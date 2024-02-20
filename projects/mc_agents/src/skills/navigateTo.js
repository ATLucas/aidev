// navigateTo.js located in ./skills

const { goals: { GoalBlock } } = require('mineflayer-pathfinder');

async function navigateTo(bot, target) {
    return new Promise((resolve, reject) => {
        const goal = new GoalBlock(target.x, target.y, target.z);
        bot.pathfinder.setGoal(goal, true);

        bot.once('goal_reached', () => {
            resolve();
        });

        bot.once('path_update', (results) => {
            if (results.status === 'noPath') {
                reject(new Error('No path to target.'));
            }
        });
    });
}

module.exports = {
    navigateTo
};
