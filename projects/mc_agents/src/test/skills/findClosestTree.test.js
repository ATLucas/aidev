// findClosestTree.test.js located in ./test/skills

const { findClosestTree } = require('../../skills/findClosestTree');
const { BotMock } = require('../mocks/botMock');
const Vec3 = require('vec3');

jest.mock('mineflayer');

describe('findClosestTree function tests', () => {
    let bot;

    beforeEach(() => {
        bot = new BotMock();
        // Simulate the findBlock method more accurately
        bot.findBlock = jest.fn().mockImplementation((options) => {
            // Assuming options.matching is a function that should return true for matching blocks
            const simulatedBlock = { position: new Vec3(100, 64, -50) };
            // Directly calling options.matching to simulate findBlock's behavior
            if (options.matching({ name: 'oak_log' })) { // Simulate finding an 'oak_log'
                return simulatedBlock;
            }
            return null;
        });
    });

    test('should find the closest tree base correctly', async () => {
        const closestTree = await findClosestTree(bot);
        // Adjust expectation to account for possible async behavior or logic within findClosestTree
        expect(closestTree).toEqual(new Vec3(100, 64, -50));
    });
});
