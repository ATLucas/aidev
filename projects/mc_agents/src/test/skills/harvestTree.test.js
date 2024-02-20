// harvestTree.test.js located in ./test/skills

const { harvestTree } = require('../../skills/harvestTree');
const { BotMock } = require('../mocks/botMock');
jest.mock('../../skills/findClosestTree', () => ({
    findClosestTree: jest.fn()
}));
jest.mock('../../skills/digBlock', () => ({
    digBlock: jest.fn().mockResolvedValue()
}));
const { findClosestTree } = require('../../skills/findClosestTree');
const { digBlock } = require('../../skills/digBlock');
const Vec3 = require('vec3');
const registry = require('prismarine-registry')('1.17.1')
const Block = require('prismarine-block')(registry)

describe('harvestTree function tests', () => {
    let bot;
    beforeEach(() => {
        jest.clearAllMocks();
        bot = new BotMock();

        // Mock blockAt to define where the tree is.
        bot.blockAt = jest.fn((pos) => {
            const baseTreePositions = (pos.y >= 60 && pos.y <= 64 && pos.x === 0 && pos.z === 0);
            const horizontalBranches = (pos.equals(new Vec3(1, 62, 0)));
            const diagonalBranches = (pos.equals(new Vec3(2, 61, 0)) || pos.equals(new Vec3(2, 63, 0)));

            if (baseTreePositions || horizontalBranches || diagonalBranches) {
                const oakLogType = 17;
                const block = new Block(oakLogType, 0, 0);
                block.name = 'oak_log'; // Manually setting for simplicity in this example
                block.position = pos;
                block.diggable = true;
                block.hardness = 2; // Example hardness
                block.canHarvest = () => true; // Simplified canHarvest method for the test
                return block;
            }
            return null;
        });
    });

    test('should find and harvest a tree', async () => {

        findClosestTree.mockResolvedValue(new Vec3(0, 60, 0)); // Simulate finding the base of a tree

        await harvestTree(bot);

        expect(findClosestTree).toHaveBeenCalled();
        expect(digBlock).toHaveBeenCalledTimes(8); // Expect digBlock to be called for each block of the tree
    });

    test('should log a message if no tree is found', async () => {
        console.log = jest.fn();
        findClosestTree.mockResolvedValue(null); // Simulate no tree found

        await harvestTree(bot);

        expect(console.log).toHaveBeenCalledWith("No tree found within range.");
        expect(digBlock).not.toHaveBeenCalled(); // digBlock should not be called if no tree is found
    });
});
