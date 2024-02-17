// gatherResource.test.js located in ./test/skills
const { BotMock } = require('../mocks/botMock');
const { navigateTo } = require('../../skills/navigateTo');
const { gatherResource } = require('../../skills/gatherResource');

jest.mock('../../skills/navigateTo', () => ({
    navigateTo: jest.fn().mockResolvedValue(true),
}));

describe('gatherResource', () => {
    let botMock;

    beforeEach(() => {
        jest.clearAllMocks();
        botMock = new BotMock();
        botMock.findBlock = jest.fn().mockImplementation(({ matching }) => {
            // Create a mock block that simulates a block that would be found
            const mockBlock = {
                name: 'oak_log',
                position: { x: 10, y: 65, z: 10 },
                dig: jest.fn().mockResolvedValue(true),
            };
        
            // Call the matching function with the mock block
            if (matching(mockBlock)) {
                return Promise.resolve(mockBlock);
            } else {
                return Promise.resolve(null);
            }
        });
        
        botMock.dig = jest.fn().mockResolvedValue(true);
    });

    it('successfully locates and harvests a wood block', async () => {
        await gatherResource(botMock, 'wood');

        // Verify that findBlock was called with the correct criteria
        expect(botMock.findBlock).toHaveBeenCalledWith(expect.objectContaining({
            matching: expect.any(Function), // The key issue is what you expect `matching` to be
            maxDistance: 64,
            point: { x: 0, y: 0, z: 0 },
        }));

        // Since findBlock is mocked to resolve, we verify if navigateTo and dig were called
        expect(navigateTo).toHaveBeenCalled();
        expect(botMock.dig).toHaveBeenCalled();
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

    // Additional tests to cover other scenarios can be added here
});
