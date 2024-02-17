// botMock.js located in ./test/mocks
const Vec3 = require('vec3');

/**
 * A mock of the mineflayer bot for unit testing purposes.
 */
class BotMock {
    constructor() {
      this.entity = {
        position: new Vec3(0, 0, 0),
        velocity: new Vec3(0, 0, 0),
      };
      this.listeners = {};
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
  }
  
  module.exports = { BotMock };
  