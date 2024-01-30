import chai from 'chai';
const expect = chai.expect;
import PolicyState from '../src/PolicyState';

describe('PolicyState', function() {
    describe('#updateState()', function() {
        it('should correctly update the internal state', function() {
            const policyState = new PolicyState();
            const actionOutcome = { action: 'harvest', result: 'success' };

            policyState.updateState(actionOutcome);

            expect(policyState.internalState.get('action')).to.equal('harvest');
            expect(policyState.internalState.get('result')).to.equal('success');
        });
    });

    describe('#resetState()', function() {
        it('should reset the internal state to its default', function() {
            const policyState = new PolicyState();
            policyState.updateState({ action: 'harvest', result: 'success' }); // Setting a state

            policyState.resetState(); // Resetting state

            expect(policyState.internalState.size).to.equal(0);
        });
    });
});
