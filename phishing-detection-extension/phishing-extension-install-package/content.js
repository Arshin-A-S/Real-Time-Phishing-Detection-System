// Extract all unique HTTP(S) links from the current page
const urls = Array.from(document.querySelectorAll("a"))
  .map(a => a.href)
  .filter(href => href.startsWith("http"));

// Send unique URLs to background for batch analysis
chrome.runtime.sendMessage({ action: "batchAnalyze", urls: [...new Set(urls)] });

chrome.runtime.onMessage.addListener((message) => {
    if (message.action === "markResults") {
      message.results.forEach(result => {
        if (result.prediction === 1) {
          // Find and mark the phishing link
          const link = document.querySelector(`a[href="${result.url}"]`);
          if (link) {
            link.style.border = "2px solid red";
            link.style.backgroundColor = "#ffe6e6";
            link.title = "Phishing detected";
          }
        }
      });
    }
  });