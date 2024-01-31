/**
 * The SensoryState class represents the environmental conditions and states relevant to the agent.
 */
class SensoryState {
    /**
     * Constructs an instance of the SensoryState class.
     */
    constructor() {
        this.isHungry = false;       // Indicates if the agent is hungry
        this.mobNearby = false;      // Indicates if there is a hostile mob nearby
        this.isNight = false;        // Indicates if it is currently nighttime
        this.isGettingLate = false;  // Indicates if it is getting late in the day
    }

    /**
     * Updates the state of the sensory properties based on the provided environmental data.
     * @param {Object} environmentalData - Data from the Minecraft environment
     */
    updateState(environmentalData) {
        if (!environmentalData || typeof environmentalData !== 'object') {
            throw new Error('Invalid environmental data provided');
        }

        // Update the properties based on environmentalData
        // This is a placeholder logic and should be replaced with real environmental data handling
        this.isNight = environmentalData.isNight;
        this.isHungry = environmentalData.isHungry;
        this.mobNearby = environmentalData.mobNearby;
        this.isGettingLate = environmentalData.isGettingLate;
    }
}

export default SensoryState;
