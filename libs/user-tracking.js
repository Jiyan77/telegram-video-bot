// Track user interactions with the bot

// Store new user in the user database
function trackUser(userId, username, firstName){
  // Check if user already exists
  let user = User.getProperty(userId.toString());
  
  if(!user){
    // User doesn't exist, create new user entry
    user = {
      id: userId,
      username: username || null,
      first_name: firstName || null,
      joined_date: (new Date()).toISOString(),
      last_activity: (new Date()).toISOString()
    };
  }else{
    // User exists, update last activity
    user.last_activity = (new Date()).toISOString();
    
    // Update username and first name if provided
    if(username) user.username = username;
    if(firstName) user.first_name = firstName;
  }
  
  // Save user data
  User.setProperty(userId.toString(), user, "json");
}

// Get all users for broadcasts
function getAllUsers(){
  // This function would be implemented by Bots.Business system
  // Users are tracked by the platform
  return null;
}

// Export functions for use in other scripts
publish({
  trackUser: trackUser,
  getAllUsers: getAllUsers
});