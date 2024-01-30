const assert = require('assert');
import SensoryState from '../src/SensoryState';

describe('SensoryState', function() {
    describe('#updateState()', function() {
        it('should update sensory states based on environmental data', function() {
            const sensoryState = new SensoryState();
            const environmentalData = {
                isHungry: true,
                mobNearby: false,
                isNight: true,
                isGettingLate: false
            };

            sensoryState.updateState(environmentalData);

            assert.strictEqual(sensoryState.isHungry, environmentalData.isHungry);
            assert.strictEqual(sensoryState.mobNearby, environmentalData.mobNearby);
            assert.strictEqual(sensoryState.isNight, environmentalData.isNight);
            assert.strictEqual(sensoryState.isGettingLate, environmentalData.isGettingLate);
        });

        it('should throw an error for invalid environmental data', function() {
            const sensoryState = new SensoryState();
            assert.throws(() => {
                sensoryState.updateState(null); // Passing null to simulate invalid data
            }, Error);
        });
    });
});
