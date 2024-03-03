// come.js located in ./skills

const { goNear } = require('./goNear');
const { PLAYER_NAME } = require('../config.js');

async function come(bot, playerName=PLAYER_NAME) {
    const player = bot.players[playerName]?.entity;
    if (!player) {
        console.log(`Player ${playerName} not found`);
        return false;
    }
    await goNear(bot, player.position);
    return true;
}

module.exports = {
    come
};
