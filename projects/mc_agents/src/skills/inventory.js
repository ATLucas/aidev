// inventory.js located in ./skills

function queryInventory(bot) {
    // Initialize an object to hold the summary
    const summary = {};
  
    // Iterate over each item in the bot's inventory
    bot.inventory.items().forEach(item => {
      // Check if the item type is already in the summary
      if (summary[item.name]) {
        // If it is, increment the count by the item's count
        summary[item.name] += item.count;
      } else {
        // If it's not, add it to the summary with its count
        summary[item.name] = item.count;
      }
    });
  
    // Log the summary to the console and return
    console.log(`Inventory: ${JSON.stringify(summary, null, 2)}`);
    return JSON.stringify(summary);
  }

  module.exports = {
      queryInventory
  };
  