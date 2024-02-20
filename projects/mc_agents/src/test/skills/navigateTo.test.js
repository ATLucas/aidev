// navigateTo.test.js located in ./test/skills

const { navigateTo } = require('../../skills/navigateTo');
const { BotMock } = require('../mocks/botMock');
const { GoalBlock } = require('mineflayer-pathfinder').goals;

describe('navigateTo function tests', () => {
    let bot;

    beforeEach(() => {
        bot = new BotMock();
        bot.pathfinder = { setGoal: jest.fn() };
        bot.once = jest.fn((event, callback) => {
            if (event === 'goal_reached') {
                process.nextTick(callback); // Simulate immediate goal reach
            }
        });
    });

    test('should set correct GoalBlock on bot.pathfinder and resolve upon reaching goal', async () => {
        const target = { x: 100, y: 64, z: -50 };

        await navigateTo(bot, target); // This will now return a promise

        expect(bot.pathfinder.setGoal).toHaveBeenCalledWith(expect.any(GoalBlock), true);
        expect(bot.pathfinder.setGoal.mock.calls[0][0].x).toBe(target.x);
        expect(bot.pathfinder.setGoal.mock.calls[0][0].y).toBe(target.y);
        expect(bot.pathfinder.setGoal.mock.calls[0][0].z).toBe(target.z);
    });

    test('should reject if no path to target is found', async () => {
        // Override the bot.once to simulate 'path_update' with 'noPath'
        bot.once = jest.fn((event, callback) => {
            if (event === 'path_update') {
                process.nextTick(() => callback({ status: 'noPath' }));
            }
        });

        const target = { x: 200, y: 64, z: -150 };

        await expect(navigateTo(bot, target)).rejects.toThrow('No path to target.');
    });
});
