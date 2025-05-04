// This code runs in the background and listens
function isGoogleSearch(url) {
  const parsedUrl = new URL(url);
  const domain = parsedUrl.hostname;
  const path = parsedUrl.pathname;
  return domain.startsWith("www.google.") && path === "/search";
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "batchAnalyze") {
    //Skip if the current page is the google search page
    if(sender.tab && isGoogleSearch(sender.tab.url)){
      return;
    }
    const urls = [...new Set(message.urls)];

    fetch("http://127.0.0.1:5000/batch_predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ urls: urls })
    })
    .then(res => res.json())
    .then(results => {
      // Filter only the phishing URLs (prediction === 1)
      const phishingUrls = results
        .filter(result => result.prediction === 1)
        .map(result => result.url);

      // Check if phishing URLs were found
      if (phishingUrls.length > 0) {
        const messageText = phishingUrls.slice(0, 5).join('\n') + 
          (phishingUrls.length > 5 ? `\n+${phishingUrls.length - 5} more` : '');

        // Create the notification with the phishing URLs
        chrome.notifications.create({
          type: "basic",
          iconUrl: "assets/icon128.png",
          title: "Phishing Links Detected!",
          message: messageText,
          priority: 2
        });
      } else {
        // If no phishing URLs found, you could optionally create a "clean" notification
        chrome.notifications.create({
          type: "basic",
          iconUrl: "assets/icon128.png",
          title: "No Phishing Links Found",
          message: "This page looks clean.",
          priority: 1
        });
      }
    })
    .catch(err => {
      console.error("Error in batch prediction:", err);
      chrome.notifications.create({
        type: "basic",
        iconUrl: "assets/icon128.png",
        title: "Error",
        message: "Could not connect to detection server.",
        priority: 2
      });
    });
  }
});
