/**
 * The PolicyState class maintains the internal state of the agent's policies.
 */
class PolicyState {
    /**
     * Constructs an instance of the PolicyState class.
     */
    constructor() {
        this.internalState = new Map(); // Stores various state information
    }

    /**
     * Updates the internal state based on the outcome of the agent's actions.
     * @param {Object} actionOutcome - Data about the result of an action taken by the agent
     */
    updateState(actionOutcome) {
        this.internalState.set('action', actionOutcome.action);
        this.internalState.set('result', actionOutcome.result);
    }

    /**
     * Resets the internal state to its default or initial values.
     */
    resetState() {
        this.internalState.clear();
    }
}

export default PolicyState;
