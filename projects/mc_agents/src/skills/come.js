// come.js located in ./skills

const { goNear } = require('./goNear');
const { PLAYER_NAME } = require('../config.js');

async function come(bot, playerName=PLAYER_NAME) {
    const player = bot.players[playerName]?.entity;
    if (!player) {
        const errMsg = `Player ${playerName} not found`;
        console.log(`INFO: ${errMsg}`);
        return {success: false, error: errMsg};
    }
    await goNear(bot, player.position);
    return {success: true};
}

module.exports = {
    come
};
