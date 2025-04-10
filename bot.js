/*CMD
  command: /start
  help: Welcome message when bot is started
  need_reply: 
  auto_retry_time: 
  folder: 
  answer: 
  keyboard: 
  aliases: 
CMD*/

let inlineKeyboard = [
  [{ text: "ব্যাকআপ চ্যানেল", url: "https://t.me/+exNiJX3B_1AzNjdh" }]
]

Bot.sendInlineKeyboard(
  inlineKeyboard,
  "This is a video sender bot. This bot send anonymously 18+ desi video to দেশি ভিডিও group. " +
  "please upload desi video only.\n\n" +
  "This bot is made by @your_next1."
)

/*CMD
  command: /help
  help: Show help instructions
  need_reply: 
  auto_retry_time: 
  folder: 
  answer: 
  keyboard: 
  aliases: 
CMD*/

let helpKeyboard = [
  [{ text: "ব্যাকআপ চ্যানেল", url: "https://t.me/+exNiJX3B_1AzNjdh" }]
]

Bot.sendInlineKeyboard(
  helpKeyboard,
  "This is a video sender bot. This bot send anonymously 18+ desi video to দেশি ভিডিও group. " +
  "please upload desi video only.\n\n" +
  "This bot is made by @your_next1."
)

/*CMD
  command: Video
  help: Handle video uploads and forward them anonymously
  need_reply: 
  auto_retry_time: 
  folder: 
  answer: 
  keyboard: 
  aliases: 
CMD*/

// টার্গেট গ্রুপ আইডি
let targetGroupId = "-1002300932976"; 

// ভিডিও চেক
if(request.video){
  // ক্যাপশন চেক
  if(request.caption){
    if(request.caption.includes("http") || request.caption.includes("t.me")){
      Bot.sendMessage("Please remove any links from the video caption and try again.");
      return;
    }
    // যেকোনো ক্যাপশন বাতিল
    Bot.sendMessage("Please remove caption text from the video and try again.");
    return;
  }

  // ভিডিও ফরওয়ার্ড করা
  Api.sendVideo({
    chat_id: targetGroupId,
    video: request.video.file_id,
    supports_streaming: true
  });

  Bot.sendMessage("Your video has been anonymously shared to the group!");
} else {
  Bot.sendMessage("Please upload only desi video.");
}

/*CMD
  command: Photo
  help: Reject photo uploads
  need_reply: 
  auto_retry_time: 
  folder: 
  answer: Please upload only desi video.
  keyboard: 
  aliases: 
CMD*/

/*CMD
  command: Document
  help: Reject document uploads
  need_reply: 
  auto_retry_time: 
  folder: 
  answer: Please upload only desi video.
  keyboard: 
  aliases: 
CMD*/

/*CMD
  command: Audio
  help: Reject audio uploads
  need_reply: 
  auto_retry_time: 
  folder: 
  answer: Please upload only desi video.
  keyboard: 
  aliases: 
CMD*/

/*CMD
  command: Voice
  help: Reject voice uploads
  need_reply: 
  auto_retry_time: 
  folder: 
  answer: Please upload only desi video.
  keyboard: 
  aliases: 
CMD*/

/*CMD
  command: Animation
  help: Reject animation uploads
  need_reply: 
  auto_retry_time: 
  folder: 
  answer: Please upload only desi video.
  keyboard: 
  aliases: 
CMD*/

/*CMD
  command: Sticker
  help: Reject sticker uploads
  need_reply: 
  auto_retry_time: 
  folder: 
  answer: Please upload only desi video.
  keyboard: 
  aliases: 
CMD*/

/*CMD
  command: BroadcastToAll
  help: Broadcast message to all users
  need_reply: 
  auto_retry_time: 
  folder: 
  answer: Broadcasting started...
  keyboard: 
  aliases: 
CMD*/

// Admin এর user_id
let adminUserId = 5534762098; // your_next1 user ID

if(user.telegramid != adminUserId){
  Bot.sendMessage("Sorry, you are not authorized to use this command.");
  return;
}

let broadcastKeyboard = [
  [{ text: "ব্যাকআপ চ্যানেল", url: "https://t.me/+exNiJX3B_1AzNjdh" }]
]

let message = "ভিডিও আনলক করতে আমাদের ব্যাকআপ " +
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
})

/*CMD
  command: SendBroadcastMessage
  help: Internal command to send broadcast messages
  need_reply: 
  auto_retry_time: 
  folder: 
  answer: 
  keyboard: 
  aliases: 
CMD*/

// Get message and keyboard from options
let msg = options.message;
let kbd = options.keyboard;

// Send message with inline keyboard
Api.sendMessage({
  chat_id: user.telegramid,
  text: msg,
  reply_markup: { inline_keyboard: kbd }
});