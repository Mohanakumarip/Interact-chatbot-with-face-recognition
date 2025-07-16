// // // // // console.log("🟢 SIA chat.js with face + voice integration");

// // // // // const subtitleDiv = document.getElementById('subtitles');
// // // // // const voiceSelect = document.getElementById('voiceSelect');
// // // // // const stopBtn = document.getElementById('stopBtn');
// // // // // const video = document.getElementById('video');
// // // // // const canvas = document.getElementById('canvas');

// // // // // const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
// // // // // const synth = window.speechSynthesis;

// // // // // let selectedVoice = null;
// // // // // let voices = [];
// // // // // let isSpeaking = false;
// // // // // let faceRecognized = false;

// // // // // // 🔊 Load available voices
// // // // // function loadVoicesAndSelect(defaultVoice = 'Google UK English Female') {
// // // // //   return new Promise((resolve) => {
// // // // //     function setVoices() {
// // // // //       voices = synth.getVoices();
// // // // //       voiceSelect.innerHTML = '';
// // // // //       voices.forEach((voice, index) => {
// // // // //         const option = document.createElement('option');
// // // // //         option.value = index;
// // // // //         option.textContent = `${voice.name} (${voice.lang})`;
// // // // //         if (voice.name.includes(defaultVoice)) {
// // // // //           option.selected = true;
// // // // //           selectedVoice = voice;
// // // // //         }
// // // // //         voiceSelect.appendChild(option);
// // // // //       });
// // // // //       resolve();
// // // // //     }

// // // // //     if (synth.getVoices().length > 0) {
// // // // //       setVoices();
// // // // //     } else {
// // // // //       synth.onvoiceschanged = setVoices;
// // // // //     }
// // // // //   });
// // // // // }

// // // // // // 🔊 Speak text
// // // // // function speakText(text) {
// // // // //   const utterance = new SpeechSynthesisUtterance(text);
// // // // //   utterance.voice = selectedVoice;
// // // // //   utterance.rate = 1;
// // // // //   utterance.pitch = 1;

// // // // //   utterance.onstart = () => {
// // // // //     isSpeaking = true;
// // // // //     stopBtn.disabled = false;
// // // // //   };
// // // // //   utterance.onend = () => {
// // // // //     isSpeaking = false;
// // // // //     stopBtn.disabled = true;
// // // // //     subtitleDiv.innerText = '';
// // // // //   };

// // // // //   synth.speak(utterance);
// // // // // }

// // // // // // 🎭 Recognize face from webcam
// // // // // async function recognizeFaceOnce() {
// // // // //   const ctx = canvas.getContext('2d');
// // // // //   canvas.width = video.videoWidth;
// // // // //   canvas.height = video.videoHeight;
// // // // //   ctx.drawImage(video, 0, 0);

// // // // //   const blob = await new Promise((res) => canvas.toBlob(res, 'image/jpeg'));
// // // // //   const formData = new FormData();
// // // // //   formData.append('file', blob, 'frame.jpg');

// // // // //   try {
// // // // //     const res = await fetch('/recognize-face', { method: 'POST', body: formData });
// // // // //     const data = await res.json();

// // // // //     if (data.success) {
// // // // //       faceRecognized = true;
// // // // //       const greeting = data.greeting || `Hey ${data.name}, how can I assist you today?`;
// // // // //       subtitleDiv.innerText = greeting;
// // // // //       speakText(greeting);

// // // // //       if (data.audio_base64) {
// // // // //         const audio = new Audio("data:audio/mp3;base64," + data.audio_base64);
// // // // //         audio.play();
// // // // //       }

// // // // //       setTimeout(startVoiceRecognition, 4000); // Let greeting finish
// // // // //     } else {
// // // // //       subtitleDiv.innerText = "Face not recognized. Please try again.";
// // // // //       setTimeout(recognizeFaceOnce, 3000);
// // // // //     }

// // // // //   } catch (err) {
// // // // //     console.error("❌ Face recognition error:", err);
// // // // //     subtitleDiv.innerText = "Error during face recognition.";
// // // // //   }
// // // // // }

// // // // // // 🗣️ Start voice interaction
// // // // // function startVoiceRecognition() {
// // // // //   if (!SpeechRecognition || !synth) {
// // // // //     alert("Your browser doesn't support speech features.");
// // // // //     return;
// // // // //   }

// // // // //   const recognition = new SpeechRecognition();
// // // // //   recognition.continuous = true;
// // // // //   recognition.lang = 'en-US';
// // // // //   recognition.interimResults = false;

// // // // //   recognition.onstart = () => console.log("🎤 Voice recognition started");
// // // // //   recognition.onerror = e => console.error("❌ Error:", e.error);
// // // // //   recognition.onend = () => {
// // // // //     if (faceRecognized) {
// // // // //       console.warn("🔁 Restarting voice recognition...");
// // // // //       recognition.start();
// // // // //     }
// // // // //   };

// // // // //   recognition.onresult = async (event) => {
// // // // //     const transcript = event.results[event.results.length - 1][0].transcript.trim();
// // // // //     subtitleDiv.innerText = `You: ${transcript}`;

// // // // //     if (isSpeaking) {
// // // // //       synth.cancel();
// // // // //       isSpeaking = false;
// // // // //       stopBtn.disabled = true;
// // // // //     }

// // // // //     const res = await fetch('/ask', {
// // // // //       method: 'POST',
// // // // //       headers: { 'Content-Type': 'application/json' },
// // // // //       body: JSON.stringify({ question: transcript })
// // // // //     });

// // // // //     const data = await res.json();
// // // // //     let reply = data.answer || "I'm not sure how to answer that.";
// // // // //     subtitleDiv.innerText = `SIA: ${reply}`;
// // // // //     speakText(reply);
// // // // //   };

// // // // //   recognition.start();
// // // // // }

// // // // // // 🔘 Event listeners
// // // // // voiceSelect.addEventListener('change', () => {
// // // // //   selectedVoice = voices[parseInt(voiceSelect.value)];
// // // // // });

// // // // // stopBtn.addEventListener('click', () => {
// // // // //   synth.cancel();
// // // // //   isSpeaking = false;
// // // // //   stopBtn.disabled = true;
// // // // //   subtitleDiv.innerText = '';
// // // // // });

// // // // // // 🚀 Init everything
// // // // // (async function init() {
// // // // //   await loadVoicesAndSelect();

// // // // //   const urlParams = new URLSearchParams(window.location.search);
// // // // //   const name = urlParams.get("name");

// // // // //   if (name && name !== "Guest") {
// // // // //     // 🟢 Face already recognized from index.html
// // // // //     faceRecognized = true;

// // // // //     const greeting = `Hey ${name}, how can I assist you today?`;
// // // // //     subtitleDiv.innerText = greeting;
// // // // //     speakText(greeting);

// // // // //     setTimeout(startVoiceRecognition, 4000);
// // // // //     return;
// // // // //   }

// // // // //   // 🔁 Fallback: recognize face here
// // // // //   navigator.mediaDevices.getUserMedia({ video: true })
// // // // //     .then((stream) => {
// // // // //       video.srcObject = stream;
// // // // //       video.onloadeddata = () => {
// // // // //         setTimeout(recognizeFaceOnce, 1000);
// // // // //       };
// // // // //     })
// // // // //     .catch((err) => {
// // // // //       console.error("❌ Camera error:", err);
// // // // //       subtitleDiv.innerText = "Camera not accessible.";
// // // // //     });
// // // // // })();


// // // // // // //working // // //
// // // // console.log("🟢 SIA chat.js with face + voice integration");

// // // // const subtitleDiv = document.getElementById('subtitles');
// // // // const voiceSelect = document.getElementById('voiceSelect');
// // // // const stopBtn = document.getElementById('stopBtn');
// // // // const video = document.getElementById('video');
// // // // const canvas = document.getElementById('canvas');

// // // // const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
// // // // const synth = window.speechSynthesis;

// // // // let selectedVoice = null;
// // // // let voices = [];
// // // // let isSpeaking = false;
// // // // let faceRecognized = false;
// // // // let exiting = false;  // 🚨 NEW

// // // // // Load available voices
// // // // function loadVoicesAndSelect(defaultVoice = 'Google UK English Female') {
// // // //   return new Promise((resolve) => {
// // // //     function setVoices() {
// // // //       voices = synth.getVoices();
// // // //       voiceSelect.innerHTML = '';
// // // //       voices.forEach((voice, index) => {
// // // //         const option = document.createElement('option');
// // // //         option.value = index;
// // // //         option.textContent = `${voice.name} (${voice.lang})`;
// // // //         if (voice.name.includes(defaultVoice)) {
// // // //           option.selected = true;
// // // //           selectedVoice = voice;
// // // //         }
// // // //         voiceSelect.appendChild(option);
// // // //       });
// // // //       resolve();
// // // //     }

// // // //     if (synth.getVoices().length > 0) {
// // // //       setVoices();
// // // //     } else {
// // // //       synth.onvoiceschanged = setVoices;
// // // //     }
// // // //   });
// // // // }

// // // // function speakText(text) {
// // // //   const utterance = new SpeechSynthesisUtterance(text);
// // // //   utterance.voice = selectedVoice;
// // // //   utterance.rate = 1;
// // // //   utterance.pitch = 1;

// // // //   utterance.onstart = () => {
// // // //     isSpeaking = true;
// // // //     stopBtn.disabled = false;
// // // //   };
// // // //   utterance.onend = () => {
// // // //     isSpeaking = false;
// // // //     stopBtn.disabled = true;
// // // //     subtitleDiv.innerText = '';
// // // //   };

// // // //   synth.speak(utterance);
// // // // }

// // // // // Face recognition
// // // // async function recognizeFaceOnce() {
// // // //   const ctx = canvas.getContext('2d');
// // // //   canvas.width = video.videoWidth;
// // // //   canvas.height = video.videoHeight;
// // // //   ctx.drawImage(video, 0, 0);

// // // //   const blob = await new Promise((res) => canvas.toBlob(res, 'image/jpeg'));
// // // //   const formData = new FormData();
// // // //   formData.append('file', blob, 'frame.jpg');

// // // //   try {
// // // //     const res = await fetch('/recognize-face', { method: 'POST', body: formData });
// // // //     const data = await res.json();

// // // //     if (data.success) {
// // // //       faceRecognized = true;
// // // //       const greeting = data.greeting || `Hey ${data.name}, how can I assist you today?`;
// // // //       subtitleDiv.innerText = greeting;
// // // //       speakText(greeting);

// // // //       if (data.audio_base64) {
// // // //         const audio = new Audio("data:audio/mp3;base64," + data.audio_base64);
// // // //         audio.play();
// // // //       }

// // // //       setTimeout(startVoiceRecognition, 4000);
// // // //     } else {
// // // //       subtitleDiv.innerText = "Face not recognized. Please try again.";
// // // //       setTimeout(recognizeFaceOnce, 3000);
// // // //     }

// // // //   } catch (err) {
// // // //     console.error("❌ Face recognition error:", err);
// // // //     subtitleDiv.innerText = "Error during face recognition.";
// // // //   }
// // // // }

// // // // // Voice recognition
// // // // function startVoiceRecognition() {
// // // //   if (!SpeechRecognition || !synth) {
// // // //     alert("Your browser doesn't support speech features.");
// // // //     return;
// // // //   }

// // // //   const recognition = new SpeechRecognition();
// // // //   recognition.continuous = true;
// // // //   recognition.lang = 'en-US';
// // // //   recognition.interimResults = false;

// // // //   recognition.onstart = () => console.log("🎤 Voice recognition started");

// // // //   recognition.onerror = e => console.error("❌ Error:", e.error);

// // // //   recognition.onend = () => {
// // // //     if (faceRecognized && !exiting) {
// // // //       console.warn("🔁 Restarting voice recognition...");
// // // //       recognition.start();
// // // //     }
// // // //   };

// // // //   recognition.onresult = async (event) => {
// // // //     const transcript = event.results[event.results.length - 1][0].transcript.trim().toLowerCase();
// // // //     subtitleDiv.innerText = `You: ${transcript}`;

// // // //     if (isSpeaking) {
// // // //       synth.cancel();
// // // //       isSpeaking = false;
// // // //       stopBtn.disabled = true;
// // // //     }

// // // //     const exitCommands = ["exit", "go back", "quit", "bye", "close"];
// // // //     if (exitCommands.some(cmd => transcript.includes(cmd))) {
// // // //       exiting = true; // 🛑 Prevent restart
// // // //       subtitleDiv.innerText = "Exiting chat. See you soon!";
// // // //       speakText("Goodbye! Redirecting you to the main screen.");
// // // //       recognition.stop();

// // // //       setTimeout(() => {
// // // //         window.location.href = "/";
// // // //       }, 3000);
// // // //       return;
// // // //     }

// // // //     try {
// // // //       const res = await fetch('/ask', {
// // // //         method: 'POST',
// // // //         headers: { 'Content-Type': 'application/json' },
// // // //         body: JSON.stringify({ question: transcript })
// // // //       });

// // // //       const data = await res.json();
// // // //       const reply = data.answer || "I'm not sure how to answer that.";
// // // //       subtitleDiv.innerText = `SIA: ${reply}`;
// // // //       speakText(reply);
// // // //     } catch (err) {
// // // //       console.error("❌ Error sending question:", err);
// // // //       subtitleDiv.innerText = "Something went wrong while asking SIA.";
// // // //     }
// // // //   };

// // // //   recognition.start();
// // // // }

// // // // // Event listeners
// // // // voiceSelect.addEventListener('change', () => {
// // // //   selectedVoice = voices[parseInt(voiceSelect.value)];
// // // // });

// // // // stopBtn.addEventListener('click', () => {
// // // //   synth.cancel();
// // // //   isSpeaking = false;
// // // //   stopBtn.disabled = true;
// // // //   subtitleDiv.innerText = '';
// // // // });

// // // // // Init
// // // // (async function init() {
// // // //   await loadVoicesAndSelect();

// // // //   const urlParams = new URLSearchParams(window.location.search);
// // // //   const name = urlParams.get("name");

// // // //   if (name && name !== "Guest") {
// // // //     faceRecognized = true;
// // // //     const greeting = `Hey ${name}, how can I assist you today?`;
// // // //     subtitleDiv.innerText = greeting;
// // // //     speakText(greeting);

// // // //     setTimeout(startVoiceRecognition, 4000);
// // // //     return;
// // // //   }

// // // //   navigator.mediaDevices.getUserMedia({ video: true })
// // // //     .then((stream) => {
// // // //       video.srcObject = stream;
// // // //       video.onloadeddata = () => {
// // // //         setTimeout(recognizeFaceOnce, 1000);
// // // //       };
// // // //     })
// // // //     .catch((err) => {
// // // //       console.error("❌ Camera error:", err);
// // // //       subtitleDiv.innerText = "Camera not accessible.";
// // // //     });
// // // // })();
// // // // // // //working // // //

// // // // // // camera is not stoping// // //
// // // console.log("🟢 SIA chat.js with dynamic greeting + face + voice integration");

// // // const subtitleDiv = document.getElementById('subtitles');
// // // const voiceSelect = document.getElementById('voiceSelect');
// // // const stopBtn = document.getElementById('stopBtn');
// // // const video = document.getElementById('video');
// // // const canvas = document.getElementById('canvas');

// // // const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
// // // const synth = window.speechSynthesis;

// // // let selectedVoice = null;
// // // let voices = [];
// // // let isSpeaking = false;
// // // let faceRecognized = false;
// // // let exiting = false;

// // // // 🎤 Load voices
// // // function loadVoicesAndSelect(defaultVoice = 'Google UK English Female') {
// // //   return new Promise((resolve) => {
// // //     function setVoices() {
// // //       voices = synth.getVoices();
// // //       voiceSelect.innerHTML = '';
// // //       voices.forEach((voice, index) => {
// // //         const option = document.createElement('option');
// // //         option.value = index;
// // //         option.textContent = `${voice.name} (${voice.lang})`;
// // //         if (voice.name.includes(defaultVoice)) {
// // //           option.selected = true;
// // //           selectedVoice = voice;
// // //         }
// // //         voiceSelect.appendChild(option);
// // //       });
// // //       resolve();
// // //     }

// // //     if (synth.getVoices().length > 0) {
// // //       setVoices();
// // //     } else {
// // //       synth.onvoiceschanged = setVoices;
// // //     }
// // //   });
// // // }

// // // // 📢 Speak text
// // // function speakText(text) {
// // //   const utterance = new SpeechSynthesisUtterance(text);
// // //   utterance.voice = selectedVoice;
// // //   utterance.rate = 1;
// // //   utterance.pitch = 1;

// // //   utterance.onstart = () => {
// // //     isSpeaking = true;
// // //     stopBtn.disabled = false;
// // //   };
// // //   utterance.onend = () => {
// // //     isSpeaking = false;
// // //     stopBtn.disabled = true;
// // //     subtitleDiv.innerText = '';
// // //   };

// // //   synth.speak(utterance);
// // // }

// // // // 📷 Face recognition
// // // async function recognizeFaceOnce() {
// // //   const ctx = canvas.getContext('2d');
// // //   canvas.width = video.videoWidth;
// // //   canvas.height = video.videoHeight;
// // //   ctx.drawImage(video, 0, 0);

// // //   const blob = await new Promise((res) => canvas.toBlob(res, 'image/jpeg'));
// // //   const formData = new FormData();
// // //   formData.append('file', blob, 'frame.jpg');

// // //   try {
// // //     const res = await fetch('/recognize-face', { method: 'POST', body: formData });
// // //     const data = await res.json();

// // //     if (data.success) {
// // //       faceRecognized = true;
// // //       const greeting = data.greeting || `Hey ${data.name}, how can I assist you today?`;
// // //       subtitleDiv.innerText = greeting;
// // //       speakText(greeting);

// // //       if (data.audio_base64) {
// // //         const audio = new Audio("data:audio/mp3;base64," + data.audio_base64);
// // //         audio.play();
// // //       }

// // //       // 🌟 New: Redirect to dynamic greeting page
// // //       if (data.redirect_url) {
// // //         setTimeout(() => {
// // //           window.location.href = data.redirect_url;
// // //         }, 6000);
// // //         return;
// // //       }

// // //       setTimeout(startVoiceRecognition, 4000);
// // //     } else {
// // //       subtitleDiv.innerText = "Face not recognized. Please try again.";
// // //       setTimeout(recognizeFaceOnce, 3000);
// // //     }

// // //   } catch (err) {
// // //     console.error("❌ Face recognition error:", err);
// // //     subtitleDiv.innerText = "Error during face recognition.";
// // //   }
// // // }

// // // // 🎙️ Voice recognition
// // // function startVoiceRecognition() {
// // //   if (!SpeechRecognition || !synth) {
// // //     alert("Your browser doesn't support speech features.");
// // //     return;
// // //   }

// // //   const recognition = new SpeechRecognition();
// // //   recognition.continuous = true;
// // //   recognition.lang = 'en-US';
// // //   recognition.interimResults = false;

// // //   recognition.onstart = () => console.log("🎤 Voice recognition started");

// // //   recognition.onerror = e => console.error("❌ Voice recognition error:", e.error);

// // //   recognition.onend = () => {
// // //     if (faceRecognized && !exiting) {
// // //       console.warn("🔁 Restarting voice recognition...");
// // //       recognition.start();
// // //     }
// // //   };

// // //   recognition.onresult = async (event) => {
// // //     const transcript = event.results[event.results.length - 1][0].transcript.trim().toLowerCase();
// // //     subtitleDiv.innerText = `You: ${transcript}`;

// // //     if (isSpeaking) {
// // //       synth.cancel();
// // //       isSpeaking = false;
// // //       stopBtn.disabled = true;
// // //     }

// // //     const exitCommands = ["exit", "go back", "quit", "bye", "close"];
// // //     if (exitCommands.some(cmd => transcript.includes(cmd))) {
// // //       exiting = true;
// // //       subtitleDiv.innerText = "Exiting chat. See you soon!";
// // //       speakText("Goodbye! Redirecting you to the main screen.");
// // //       recognition.stop();
// // //       setTimeout(() => window.location.href = "/", 3000);
// // //       return;
// // //     }

// // //     try {
// // //       const res = await fetch('/ask', {
// // //         method: 'POST',
// // //         headers: { 'Content-Type': 'application/json' },
// // //         body: JSON.stringify({ question: transcript })
// // //       });

// // //       const data = await res.json();
// // //       const reply = data.answer || "I'm not sure how to answer that.";
// // //       subtitleDiv.innerText = `SIA: ${reply}`;
// // //       speakText(reply);
// // //     } catch (err) {
// // //       console.error("❌ Error sending question:", err);
// // //       subtitleDiv.innerText = "Something went wrong while asking SIA.";
// // //     }
// // //   };

// // //   recognition.start();
// // // }

// // // // 🎛️ Event handlers
// // // voiceSelect.addEventListener('change', () => {
// // //   selectedVoice = voices[parseInt(voiceSelect.value)];
// // // });

// // // stopBtn.addEventListener('click', () => {
// // //   synth.cancel();
// // //   isSpeaking = false;
// // //   stopBtn.disabled = true;
// // //   subtitleDiv.innerText = '';
// // // });

// // // // 🟢 Init logic
// // // (async function init() {
// // //   await loadVoicesAndSelect();

// // //   const urlParams = new URLSearchParams(window.location.search);
// // //   const name = urlParams.get("name");

// // //   if (name && name !== "Guest") {
// // //     faceRecognized = true;
// // //     const greeting = `Hey ${name}, how can I assist you today?`;
// // //     subtitleDiv.innerText = greeting;
// // //     speakText(greeting);
// // //     setTimeout(startVoiceRecognition, 4000);
// // //     return;
// // //   }

// // //   navigator.mediaDevices.getUserMedia({ video: true })
// // //     .then((stream) => {
// // //       video.srcObject = stream;
// // //       video.onloadeddata = () => {
// // //         setTimeout(recognizeFaceOnce, 1000);
// // //       };
// // //     })
// // //     .catch((err) => {
// // //       console.error("❌ Camera error:", err);
// // //       subtitleDiv.innerText = "Camera not accessible.";
// // //     });
// // // })();
// // // // // // camera is not stoping// // //

// // console.log("🟢 Final SIA chat.js: no re-greeting, no camera if name passed");

// // const subtitleDiv = document.getElementById('subtitles');
// // const voiceSelect = document.getElementById('voiceSelect');
// // const stopBtn = document.getElementById('stopBtn');
// // const video = document.getElementById('video');
// // const canvas = document.getElementById('canvas');

// // const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
// // const synth = window.speechSynthesis;

// // let selectedVoice = null;
// // let voices = [];
// // let isSpeaking = false;
// // let faceRecognized = false;
// // let exiting = false;

// // // 🎤 Load voices
// // function loadVoicesAndSelect(defaultVoice = 'Google UK English Female') {
// //   return new Promise((resolve) => {
// //     function setVoices() {
// //       voices = synth.getVoices();
// //       voiceSelect.innerHTML = '';
// //       voices.forEach((voice, index) => {
// //         const option = document.createElement('option');
// //         option.value = index;
// //         option.textContent = `${voice.name} (${voice.lang})`;
// //         if (voice.name.includes(defaultVoice)) {
// //           option.selected = true;
// //           selectedVoice = voice;
// //         }
// //         voiceSelect.appendChild(option);
// //       });
// //       resolve();
// //     }

// //     if (synth.getVoices().length > 0) {
// //       setVoices();
// //     } else {
// //       synth.onvoiceschanged = setVoices;
// //     }
// //   });
// // }

// // // 📢 Speak text
// // function speakText(text) {
// //   const utterance = new SpeechSynthesisUtterance(text);
// //   utterance.voice = selectedVoice;
// //   utterance.rate = 1;
// //   utterance.pitch = 1;

// //   utterance.onstart = () => {
// //     isSpeaking = true;
// //     stopBtn.disabled = false;
// //   };
// //   utterance.onend = () => {
// //     isSpeaking = false;
// //     stopBtn.disabled = true;
// //     subtitleDiv.innerText = '';
// //   };

// //   synth.speak(utterance);
// // }

// // // 🎙️ Voice recognition
// // function startVoiceRecognition() {
// //   if (!SpeechRecognition || !synth) {
// //     alert("Your browser doesn't support speech features.");
// //     return;
// //   }

// //   const recognition = new SpeechRecognition();
// //   recognition.continuous = true;
// //   recognition.lang = 'en-US';
// //   recognition.interimResults = false;

// //   recognition.onstart = () => console.log("🎤 Voice recognition started");

// //   recognition.onerror = e => console.error("❌ Voice recognition error:", e.error);

// //   recognition.onend = () => {
// //     if (faceRecognized && !exiting) {
// //       console.warn("🔁 Restarting voice recognition...");
// //       recognition.start();
// //     }
// //   };

// //   recognition.onresult = async (event) => {
// //     const transcript = event.results[event.results.length - 1][0].transcript.trim().toLowerCase();
// //     subtitleDiv.innerText = `You: ${transcript}`;

// //     if (isSpeaking) {
// //       synth.cancel();
// //       isSpeaking = false;
// //       stopBtn.disabled = true;
// //     }

// //     const exitCommands = ["exit", "go back", "quit", "bye", "close"];
// //     if (exitCommands.some(cmd => transcript.includes(cmd))) {
// //       exiting = true;
// //       subtitleDiv.innerText = "Exiting chat. See you soon!";
// //       speakText("Goodbye! Redirecting you to the main screen.");
// //       recognition.stop();
// //       setTimeout(() => window.location.href = "/", 3000);
// //       return;
// //     }

// //     try {
// //       const res = await fetch('/ask', {
// //         method: 'POST',
// //         headers: { 'Content-Type': 'application/json' },
// //         body: JSON.stringify({ question: transcript })
// //       });

// //       const data = await res.json();
// //       const reply = data.answer || "I'm not sure how to answer that.";
// //       subtitleDiv.innerText = `SIA: ${reply}`;
// //       speakText(reply);
// //     } catch (err) {
// //       console.error("❌ Error sending question:", err);
// //       subtitleDiv.innerText = "Something went wrong while asking SIA.";
// //     }
// //   };

// //   recognition.start();
// // }

// // // 🎛️ Event listeners
// // voiceSelect.addEventListener('change', () => {
// //   selectedVoice = voices[parseInt(voiceSelect.value)];
// // });

// // stopBtn.addEventListener('click', () => {
// //   synth.cancel();
// //   isSpeaking = false;
// //   stopBtn.disabled = true;
// //   subtitleDiv.innerText = '';
// // });

// // // 🟢 Init logic
// // (async function init() {
// //   await loadVoicesAndSelect();

// //   const urlParams = new URLSearchParams(window.location.search);
// //   const name = urlParams.get("name");

// //   // ✅ If redirected from greeting page, skip greeting, skip camera, go straight to voice
// //   if (name && name !== "Guest") {
// //     faceRecognized = true;

// //     // ✅ Stop camera if accidentally still running
// //     if (video.srcObject) {
// //       video.srcObject.getTracks().forEach(track => track.stop());
// //       video.srcObject = null;
// //     }

// //     setTimeout(startVoiceRecognition, 500);  // small delay to sync
// //     return;
// //   }

// //   // ❌ No name in URL – fallback to full face recognition flow
// //   navigator.mediaDevices.getUserMedia({ video: true })
// //     .then((stream) => {
// //       video.srcObject = stream;
// //       video.onloadeddata = () => {
// //         setTimeout(recognizeFaceOnce, 1000);
// //       };
// //     })
// //     .catch((err) => {
// //       console.error("❌ Camera error:", err);
// //       subtitleDiv.innerText = "Camera not accessible.";
// //     });
// // })();
// // 🟢 chat.js - Personalized Chat without Camera Recognition



// // // // not speeking // // //
// console.log("🟢 SIA chat.js initialized");

// // HTML Elements
// const subtitleDiv = document.getElementById('subtitles');
// const voiceSelect = document.getElementById('voiceSelect');
// const stopBtn = document.getElementById('stopBtn');

// const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
// const synth = window.speechSynthesis;

// let selectedVoice = null;
// let voices = [];
// let isSpeaking = false;
// let exiting = false;

// // 🔊 Load voices
// function loadVoicesAndSelect(defaultVoice = 'Google UK English Female') {
//   return new Promise((resolve) => {
//     function setVoices() {
//       voices = synth.getVoices();
//       voiceSelect.innerHTML = '';
//       voices.forEach((voice, index) => {
//         const option = document.createElement('option');
//         option.value = index;
//         option.textContent = `${voice.name} (${voice.lang})`;
//         if (voice.name.includes(defaultVoice)) {
//           option.selected = true;
//           selectedVoice = voice;
//         }
//         voiceSelect.appendChild(option);
//       });
//       resolve();
//     }

//     if (synth.getVoices().length > 0) {
//       setVoices();
//     } else {
//       synth.onvoiceschanged = setVoices;
//     }
//   });
// }

// // 📢 Speak text
// function speakText(text) {
//   const utterance = new SpeechSynthesisUtterance(text);
//   utterance.voice = selectedVoice;
//   utterance.rate = 1;
//   utterance.pitch = 1;

//   utterance.onstart = () => {
//     isSpeaking = true;
//     stopBtn.disabled = false;
//   };

//   utterance.onend = () => {
//     isSpeaking = false;
//     stopBtn.disabled = true;
//     subtitleDiv.innerText = '';
//   };

//   synth.speak(utterance);
// }

// // 🎙️ Voice recognition
// function startVoiceRecognition() {
//   if (!SpeechRecognition || !synth) {
//     alert("Your browser doesn't support speech features.");
//     return;
//   }

//   const recognition = new SpeechRecognition();
//   recognition.continuous = true;
//   recognition.lang = 'en-US';
//   recognition.interimResults = false;

//   recognition.onstart = () => console.log("🎤 Voice recognition started");

//   recognition.onerror = (e) => {
//     console.error("❌ Voice recognition error:", e.error);
//   };

//   recognition.onend = () => {
//     if (!exiting) {
//       console.warn("🔁 Restarting voice recognition...");
//       recognition.start();
//     }
//   };

//   recognition.onresult = async (event) => {
//     const transcript = event.results[event.results.length - 1][0].transcript.trim().toLowerCase();
//     subtitleDiv.innerText = `You: ${transcript}`;

//     if (isSpeaking) {
//       synth.cancel();
//       isSpeaking = false;
//       stopBtn.disabled = true;
//     }

//     const exitCommands = ["exit", "go back", "quit", "bye", "close"];
//     if (exitCommands.some(cmd => transcript.includes(cmd))) {
//       exiting = true;
//       subtitleDiv.innerText = "Exiting chat. See you soon!";
//       speakText("Goodbye! Redirecting you to the main screen.");
//       recognition.stop();
//       setTimeout(() => window.location.href = "/", 3000);
//       return;
//     }

//     try {
//       const res = await fetch('/ask', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ question: transcript })
//       });

//       const data = await res.json();
//       const reply = data.answer || "I'm not sure how to answer that.";
//       subtitleDiv.innerText = `SIA: ${reply}`;
//       speakText(reply);
//     } catch (err) {
//       console.error("❌ Error sending question:", err);
//       subtitleDiv.innerText = "Something went wrong while asking SIA.";
//     }
//   };

//   recognition.start();
// }

// // 🟢 Init
// (async function init() {
//   await loadVoicesAndSelect();

//   const urlParams = new URLSearchParams(window.location.search);
//   const name = urlParams.get("name");

//   if (name && name !== "Guest") {
//     const greeting = `Hey ${name}, how can I assist you today?`;
//     subtitleDiv.innerText = greeting;
//     speakText(greeting);
//   } else {
//     const greeting = "Hi there! How can I help you today?";
//     subtitleDiv.innerText = greeting;
//     speakText(greeting);
//   }

//   setTimeout(startVoiceRecognition, 4000);
// })();

// // 🎛️ Button events
// voiceSelect.addEventListener('change', () => {
//   selectedVoice = voices[parseInt(voiceSelect.value)];
// });

// stopBtn.addEventListener('click', () => {
//   synth.cancel();
//   isSpeaking = false;
//   stopBtn.disabled = true;
//   subtitleDiv.innerText = '';
// });
// // // // not speeking // // //
console.log("🟢 SIA Chat.js Initialized");

const subtitleDiv = document.getElementById('subtitles');
const voiceSelect = document.getElementById('voiceSelect');
const stopBtn = document.getElementById('stopBtn');

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const synth = window.speechSynthesis;

let selectedVoice = null;
let voices = [];
let isSpeaking = false;
let exiting = false;

// ✅ Load voices and select default or fallback
function loadVoicesAndSelect(defaultVoice = 'Google UK English Female') {
  return new Promise((resolve) => {
    function setVoices() {
      voices = synth.getVoices();
      console.log("🎙️ Available Voices:", voices);

      voiceSelect.innerHTML = '';
      let fallbackIndex = 0;

      voices.forEach((voice, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.textContent = `${voice.name} (${voice.lang})`;
        voiceSelect.appendChild(option);

        if (voice.name.includes(defaultVoice)) {
          option.selected = true;
          selectedVoice = voice;
        }

        if (index === 0 && !selectedVoice) {
          fallbackIndex = index;
        }
      });

      if (!selectedVoice && voices.length > 0) {
        selectedVoice = voices[fallbackIndex];
        voiceSelect.value = fallbackIndex;
      }

      resolve();
    }

    if (synth.getVoices().length > 0) {
      setVoices();
    } else {
      synth.onvoiceschanged = setVoices;
    }
  });
}

// ✅ Speak Text
function speakText(text) {
  console.log("🗣️ Speaking:", text);
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.voice = selectedVoice;
  utterance.rate = 1;
  utterance.pitch = 1;

  utterance.onstart = () => {
    isSpeaking = true;
    stopBtn.disabled = false;
  };

  utterance.onend = () => {
    isSpeaking = false;
    stopBtn.disabled = true;
    subtitleDiv.innerText = '';
  };

  synth.speak(utterance);
}

// ✅ Voice Recognition
function startVoiceRecognition() {
  if (!SpeechRecognition || !synth) {
    alert("Your browser doesn't support speech features.");
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.lang = 'en-US';
  recognition.interimResults = false;

  recognition.onstart = () => console.log("🎤 Voice recognition started");
  recognition.onerror = e => console.error("❌ Voice recognition error:", e.error);

  recognition.onend = () => {
    if (!exiting) {
      console.warn("🔁 Restarting voice recognition...");
      recognition.start();
    }
  };

  recognition.onresult = async (event) => {
    const transcript = event.results[event.results.length - 1][0].transcript.trim().toLowerCase();
    subtitleDiv.innerText = `You: ${transcript}`;

    if (isSpeaking) {
      synth.cancel();
      isSpeaking = false;
      stopBtn.disabled = true;
    }

    const exitCommands = ["exit", "go back", "quit", "bye", "close"];
    if (exitCommands.some(cmd => transcript.includes(cmd))) {
      exiting = true;
      subtitleDiv.innerText = "Exiting chat. See you soon!";
      speakText("Goodbye! Redirecting you to the main screen.");
      recognition.stop();
      setTimeout(() => window.location.href = "/", 3000);
      return;
    }

    try {
      const res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: transcript })
      });

      const data = await res.json();
      const reply = data.answer || "I'm not sure how to answer that.";
      subtitleDiv.innerText = `SIA: ${reply}`;
      speakText(reply);
    } catch (err) {
      console.error("❌ Error sending question:", err);
      subtitleDiv.innerText = "Something went wrong while asking SIA.";
    }
  };

  recognition.start();
}

// ✅ Event Listeners
voiceSelect.addEventListener('change', () => {
  selectedVoice = voices[parseInt(voiceSelect.value)];
});

stopBtn.addEventListener('click', () => {
  synth.cancel();
  isSpeaking = false;
  stopBtn.disabled = true;
  subtitleDiv.innerText = '';
});

// 🧪 Manual voice test button (optional)
window.testVoice = () => {
  speakText("This is a test voice. I am working.");
};

// ✅ Initialize on page load
(async function init() {
  await loadVoicesAndSelect();

  const urlParams = new URLSearchParams(window.location.search);
  const name = urlParams.get("name");

  if (name && name !== "Guest") {
    const greeting = `Welcome back, ${name}. How can I assist you today?`;
    subtitleDiv.innerText = greeting;
    setTimeout(() => speakText(greeting), 500);  // slight delay for autoplay policy
  } else {
    subtitleDiv.innerText = "Hi! How can I help you today?";
  }

  setTimeout(startVoiceRecognition, 1000);  // Start voice recognition after short delay
})();
