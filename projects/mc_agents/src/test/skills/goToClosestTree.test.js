// goToClosestTree.test.js located in ./test/skills

const { goToClosestTree } = require('../../skills/goToClosestTree');
const { BotMock } = require('../mocks/botMock');
jest.mock('../../skills/findClosestTree', () => ({
    findClosestTree: jest.fn()
}));
jest.mock('../../skills/navigateTo', () => ({
    navigateTo: jest.fn().mockResolvedValue()
}));
const { findClosestTree } = require('../../skills/findClosestTree');
const { navigateTo } = require('../../skills/navigateTo');
const Vec3 = require('vec3');

describe('goToClosestTree function tests', () => {
    let bot;
    beforeEach(() => {
        bot = new BotMock();
    });

    test('should call navigateTo with a position 2 blocks away from the tree when a tree is found', async () => {
        const treePosition = new Vec3(10, 65, -10);
        bot.entity.position = new Vec3(0, 65, 0); // Mock the bot's position
        findClosestTree.mockResolvedValue(treePosition);

        const expectedDirection = treePosition.minus(bot.entity.position).normalize().scale(-2);
        const expectedStopPosition = treePosition.plus(expectedDirection);
        expectedStopPosition.y = treePosition.y; // Ensure y-coordinate remains unchanged

        await goToClosestTree(bot);

        expect(navigateTo).toHaveBeenCalledWith(bot, expectedStopPosition);
    });

    test('should log a message when no tree is found', async () => {
        console.log = jest.fn(); // Mock console.log for this test
        findClosestTree.mockResolvedValue(null);

        await goToClosestTree(bot);

        expect(console.log).toHaveBeenCalledWith("No tree found within range.");
    });
});
