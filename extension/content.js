chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
  if (msg.text === 'getUrl') {
    chrome.runtime.sendMessage(
      {URL: window.location.href},
      function(response) {
        result = response.farewell;
        window.confirm(result);
      });
  }
});