// botMock.js located in ./test/mocks
const Vec3 = require('vec3');

/**
 * A mock of the mineflayer bot for unit testing purposes.
 */
class BotMock {
    constructor() {
      this.entity = {
        position: new Vec3(0, 0, 0),
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
  