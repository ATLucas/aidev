const MINECRAFT_HOST = "localhost";
const MINECRAFT_PORT = "3001";

const PLAYER_NAME = "atlucas";

const BOT_CONFIG = {
    username: "alpha",
    address: MINECRAFT_HOST,
    port: MINECRAFT_PORT,
    version: "1.20.1",
    viewDistance: "tiny",
};

const START_POINT = { x: 327, y: 68, z: 32 }; // Forest
// const START_POINT = { x: 256, y: 63, z: 6 }; // Beach

module.exports = {
    MINECRAFT_HOST,
    MINECRAFT_PORT,
    PLAYER_NAME,
    BOT_CONFIG,
    START_POINT,
};