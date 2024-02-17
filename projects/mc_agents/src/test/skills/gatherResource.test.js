// gatherResource.test.js located in ./test/skills
const { BotMock } = require('../mocks/botMock');
const { navigateTo } = require('../../skills/navigateTo');
const { gatherResource } = require('../../skills/gatherResource');
const Vec3 = require('vec3');

jest.mock('../../skills/navigateTo', () => ({
    navigateTo: jest.fn().mockResolvedValue(true),
}));

describe('gatherResource', () => {
    let botMock;

    beforeEach(() => {
        jest.clearAllMocks();
        botMock = new BotMock();
        botMock.isDigging = false; // Simulate bot's digging state
        botMock.entity.position = new Vec3(0, 0, 0); // Initial bot position
        botMock.entity.velocity = new Vec3(0, 0, 0); // Simulate bot is stationary

        // Adjust botMock.findBlock to ensure it reflects the actual behavior expected in gatherResource
        botMock.findBlock = jest.fn().mockImplementation(({ matching }) => {
            // Ensure the block is within a reasonable distance to require navigation
            const mockBlock = {
                name: 'oak_log',
                position: new Vec3(10, 0, 0),
                dig: jest.fn().mockResolvedValue(true),
            };
            return matching(mockBlock) ? mockBlock : null;
        });

        botMock.dig = jest.fn().mockImplementation(() => {
            if (botMock.isDigging) {
                return Promise.reject(new Error('Already digging'));
            } else {
                botMock.isDigging = true;
                return new Promise((resolve) => {
                    setTimeout(() => {
                        botMock.isDigging = false; // Reset digging state
                        resolve();
                    }, 100); // Simulate dig time
                });
            }
        });
    });

    it('successfully locates and harvests a wood block', async () => {
        await gatherResource(botMock, 'wood');

        expect(botMock.findBlock).toHaveBeenCalled();
        expect(navigateTo).toHaveBeenCalled(); // Ensure this check passes by adjusting mock setup
        expect(botMock.dig).toHaveBeenCalled();
    });

    it('does not attempt to dig if the bot is already digging', async () => {
        // Simulate the bot is already digging
        botMock.isDigging = true;

        await gatherResource(botMock, 'wood');
        
        // Verify that dig was not called since the bot is already digging
        expect(botMock.dig).not.toHaveBeenCalled();
    });

    it('does not attempt to dig if the bot is not close enough to the target block', async () => {
        // Adjust the bot's position to simulate being far enough away to require navigation
        botMock.entity.position = new Vec3(50, 0, 50);

        await gatherResource(botMock, 'wood');

        // In this case, navigateTo should be called, but dig should not be called because the bot is too far
        expect(navigateTo).toHaveBeenCalled(); // Ensure this check passes
        expect(botMock.dig).not.toHaveBeenCalled();
    });

    it('handles case when no resource is found', async () => {
        botMock.findBlock = jest.fn().mockReturnValue(null);

        const consoleSpy = jest.spyOn(console, 'log');
        await gatherResource(botMock, 'wood');

        expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('No wood found within search radius'));
    });

    it('handles unrecognized resource types gracefully', async () => {
        const consoleSpy = jest.spyOn(console, 'log');
        await gatherResource(botMock, 'unobtainium');

        expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Resource type unobtainium is not recognized'));
    });
});
