// navigateTo.js located in ./test/skills
const { navigateTo } = require('../../skills/navigateTo');
const { BotMock } = require('../mocks/botMock');
const { GoalBlock } = require('mineflayer-pathfinder').goals;

describe('navigateTo function tests', () => {
    test('should set correct GoalBlock on bot.pathfinder', () => {
        const bot = new BotMock();
        bot.pathfinder = { setGoal: jest.fn() };

        const target = { x: 100, y: 64, z: -50 };
        navigateTo(bot, target);

        expect(bot.pathfinder.setGoal).toHaveBeenCalledWith(expect.any(GoalBlock));
        expect(bot.pathfinder.setGoal.mock.calls[0][0].x).toBe(target.x);
        expect(bot.pathfinder.setGoal.mock.calls[0][0].y).toBe(target.y);
        expect(bot.pathfinder.setGoal.mock.calls[0][0].z).toBe(target.z);
    });
});
