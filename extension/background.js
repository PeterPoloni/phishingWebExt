chrome.action.onClicked.addListener(function (tab) {
    chrome.tabs.sendMessage(
        tab.id,
        { text: 'getUrl' }
    );
});

var host = 'http://127.0.0.1:8000';

	chrome.runtime.onMessage.addListener(
		function(request, sender, sendResponse) {

			var url = host + '/req/?URL='+ request.URL ;
			fetch(url)
			.then(response => response.json())
			.then(response => sendResponse({farewell: response}))
			.catch(error => console.log(error))
				
			return true; 
		  
	});