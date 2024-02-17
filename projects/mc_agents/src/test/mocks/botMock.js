// botMock.js located in ./test/mocks

/**
 * A mock of the mineflayer bot for unit testing purposes.
 */
class BotMock {
    constructor() {
      this.entity = {
        position: { x: 0, y: 0, z: 0 },
      };
      this.listeners = {};
    }
  
    findBlock(options) {
      // This function should be overridden in tests where specific behavior is required
      return null;
    }
  
    dig(block) {
      // This function should be overridden in tests where specific behavior is required
      return Promise.resolve(true);
    }
  
    on(eventName, listener) {
      if (!this.listeners[eventName]) {
        this.listeners[eventName] = [];
      }
      this.listeners[eventName].push(listener);
    }
  
    emit(eventName, ...args) {
      if (this.listeners[eventName]) {
        this.listeners[eventName].forEach(listener => listener(...args));
      }
    }
  
    // Additional mock methods as needed for testing
  }
  
  module.exports = { BotMock };
  