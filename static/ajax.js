 // The JavaScript Part Starts
 const contentDiv = document.querySelector('.messages');
 const btn = document.querySelector(".talk");
 const content = document.querySelector(".content");


 const YouTube = ["ne haber"];
 const SpeechRecognition =
 window.SpeechRecognition || window.webkitSpeechRecognition;
 const recognition = new SpeechRecognition();

 recognition.onstart = function () {
  btn.style.backgroundColor='red';
 };
 
 recognition.onresult = function (event) {
  btn.style.backgroundColor='white'; 
  const current = event.resultIndex;

   const transcript = event.results[current][0].transcript;
   content.textContent = transcript;
   readOutLoud(transcript);
 };

 btn.addEventListener("click", () => {
   recognition.stop();
   recognition.start();
 });

 function readOutLoud(message) {
   const speech = new SpeechSynthesisUtterance();
   speech.lang = 'en-US'; // Set the language to English


  // Create a new div element
  var you = document.createElement('p');
  // Set the responseq value as the content of the div element
  you.textContent =message;
  const myClass = 'you';
  you.classList.add(myClass);

  var messagesDiv = document.querySelector('.messages');
  messagesDiv.appendChild(you);

   PushUrl(message);
   speech.volume = 1;
   speech.rate = 1.1;
   speech.pitch = 1;

   window.speechSynthesis.speak(speech);
 }function PushUrl(message) {
  var method = "POST";
  var url = "/chat";
  var data = { message: message };
  var headers = { "Content-Type": "application/json" };

  fetch(url, {
      method: method,
      headers: headers,
      body: JSON.stringify(data)
  })
  .then(function(response) {
      if (response.ok) {
          return response.json();
      } else {
          throw new Error("AJAX request failed.");
      }
  })
  .then(function(responseJson) {
      // Add timestamp to audio URL to avoid caching
      var audioUrl = responseJson.audio_path+"?t=" + new Date().getTime();
      console.log("Response message: " + responseJson.responseq);
      // Load audio file using XMLHttpRequest
      var xhr = new XMLHttpRequest();
      xhr.open('GET', audioUrl, true);
      xhr.responseType = 'blob';
      xhr.onload = function(e) {
          if (this.status == 200) {
              var blob = this.response;
              // Create URL from blob
              var objectUrl = URL.createObjectURL(blob);
              // Create new Audio object using URL
              var audio = new Audio(objectUrl);
              // Play audio file
              audio.play();
          }
      };
    // Create a new div element
    var div = document.createElement('p');
    // Set the responseq value as the content of the div element
    div.textContent =responseJson.responseq;
    const myClass = 'chatbot';
    div.classList.add(myClass);  
    var messagesDiv = document.querySelector('.messages');
  
    messagesDiv.appendChild(div);
    messagesDiv.scrollTop=messagesDiv.scrollHeight;
      xhr.send();
      
  })
  .catch(function(error) {
      console.log("Error: " + error);
  });
}
