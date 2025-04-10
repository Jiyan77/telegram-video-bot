// Set up scheduled broadcasts
// Automatically broadcast to all users every 24 hours

// Schedule broadcast task
function setupDailyBroadcast() {
  // Create a task that runs once per day
  Bot.setInterval({
    interval: 24 * 60 * 60, // 24 hours in seconds
    run: sendBroadcastToAll
  });
}

// Send broadcast to all users
function sendBroadcastToAll() {
  let broadcastKeyboard = [
    [{ text: "ব্যাকআপ চ্যানেল", url: "https://t.me/+exNiJX3B_1AzNjdh" }]
  ];

  let message = 
    "ভিডিও আনলক করতে আমাদের ব্যাকআপ " +
    "চ্যানেলে জয়েন করুন। সরাসরি ভিডিও " +
    "দেওয়ার কারণে যে কোনো সময় আমাদের " +
    "গ্রুপ ব্যান হতে পারে তাই অবশ্যই ব্যাকআপ " +
    "গ্রুপে জয়েন থাকবেন।\n\n" +
    "Please join our backup group to stay with us. Click on the \"Backup Channel\" button to join our backup.";

  // Broadcast to all users
  Bot.runAll({
    command: "SendBroadcastMessage",
    options: {
      message: message,
      keyboard: broadcastKeyboard
    }
  });
}

// Start the scheduled broadcasts
setupDailyBroadcast();

// Make functions available for import
publish({
  sendBroadcastToAll: sendBroadcastToAll
});