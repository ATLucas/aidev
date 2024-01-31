// Example test structure

import { expect } from 'chai';
import SurvivalPolicy from '../src/policies/SurvivalPolicy.js';
import SensoryState from '../src/SensoryState.js';
import PolicyState from '../src/PolicyState.js';

describe('SurvivalPolicy', function() {
    let sensoryState, policyState, survivalPolicy;

    beforeEach(function() {
        sensoryState = new SensoryState();
        policyState = new PolicyState();
        survivalPolicy = new SurvivalPolicy();
    });

    it('should set findShelter action when it is night', function() {
        sensoryState.updateState({ isNight: true, mobNearby: false });
        survivalPolicy.applyPolicy(sensoryState, policyState);
        expect(policyState.internalState.get('action')).to.equal('findShelter');
    });

    it('should set avoidCombat action when a mob is nearby', function() {
        sensoryState.updateState({ isNight: false, mobNearby: true });
        survivalPolicy.applyPolicy(sensoryState, policyState);
        expect(policyState.internalState.get('action')).to.equal('avoidCombat');
    });
});
