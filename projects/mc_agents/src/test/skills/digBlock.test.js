// digBlock.test.js located in ./test/skills

const { digBlock } = require('../../skills/digBlock');
const { BotMock } = require('../mocks/botMock');
const registry = require('prismarine-registry')('1.17.1')
const Block = require('prismarine-block')(registry)
const Vec3 = require('vec3');

describe('digBlock function tests', () => {
    let bot;
    let block;

    beforeEach(() => {
        jest.clearAllMocks();
        bot = new BotMock();
        bot.canDigBlock = jest.fn();
        bot.dig = jest.fn().mockImplementation((block, callback) => process.nextTick(callback));

        block = new Block(registry.blocksByName.dirt);
        block.position = Vec3(0, 0, 0)

        bot.once = jest.fn((event, handler) => {
            // Simulate the diggingCompleted event immediately for simplicity
            if (event === 'diggingCompleted') process.nextTick(() => handler(block));
        });
    });

    test('should call bot.dig with the correct block when the block is diggable', async () => {
        bot.canDigBlock.mockReturnValue(true);

        await digBlock(bot, block);

        expect(bot.dig).toHaveBeenCalledWith(block, expect.any(Function));
    });

    test('should wait to complete until the block has been dug', async () => {
        bot.canDigBlock.mockReturnValue(true);

        const promise = digBlock(bot, block);
        await expect(promise).resolves.toBeUndefined();
    });

    test('should log a message if the block cannot be dug', async () => {
        bot.canDigBlock.mockReturnValue(false);
        console.log = jest.fn();

        await digBlock(bot, block);

        expect(console.log).toHaveBeenCalledWith("Cannot dig this block:", block.name);
    });
});
