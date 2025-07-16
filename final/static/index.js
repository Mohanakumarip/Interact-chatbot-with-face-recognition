// // // //working // // //
// // let slideIndex = 0;
// // const slides = document.getElementsByClassName("slide");
// // const botAvatar = document.getElementById("bot-avatar");
// // const botStatus = document.getElementById('bot-status');
// // const siaOutput = document.getElementById('sia-output');
// // const video = document.getElementById('video');
// // const canvas = document.getElementById('canvas');

// // function showSlides() {
// //   for (let slide of slides) {
// //     slide.style.display = "none";
// //   }

// //   slideIndex = (slideIndex + 1) % slides.length;
// //   slides[slideIndex].style.display = "block";

// //   const isLastSlide = slideIndex === slides.length - 1;

// //   botAvatar.src = isLastSlide
// //     ? "/static/registration_qr.png"
// //     : "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnZ2ZjN2N3Z1d3pqaHloaXdmaG9qcmhkNXo1NW5ldmxmMGdpaXlwNSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/VDMHgvx8N9U7UUlczQ/giphy.gif";

// //   const delay = isLastSlide ? 8000 : 3000;
// //   setTimeout(showSlides, delay);
// // }

// // showSlides();

// // // 🎤 Voice wake word logic
// // const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

// // if (!SpeechRecognition) {
// //   alert("Your browser does not support Speech Recognition. Please use Google Chrome.");
// // } else {
// //   const recognition = new SpeechRecognition();
// //   recognition.continuous = true;
// //   recognition.lang = 'en-US';
// //   recognition.interimResults = false;

// //   recognition.onstart = () => {
// //     console.log("🎤 Voice recognition started");
// //     siaOutput.innerText = "🎤 Listening...";
// //   };

// //   recognition.onresult = async (event) => {
// //     const transcript = event.results[event.results.length - 1][0].transcript.trim().toLowerCase();
// //     console.log("🗣️ Heard:", transcript);
// //     siaOutput.innerText = `You said: "${transcript}"`;

// //     const triggers = ["hi sia", "hello sia", "hey sia", "ok sia", "start sia", 'siya', 'sia', "hi siya", "hello siya", "hey siya", "ok siya", "start siya"];
// //     if (triggers.some(trigger => transcript.includes(trigger))) {
// //       botStatus.innerText = "🟢 Wake word detected. Recognizing face...";
// //       await startCameraAndRecognizeFace();
// //     }
// //   };

// //   recognition.onerror = (e) => {
// //     console.error("❌ Recognition error:", e);
// //     siaOutput.innerText = "Error: " + e.error;
// //   };

// //   recognition.onend = () => {
// //     console.warn("🔁 Restarting recognition...");
// //     recognition.start();
// //   };

// //   recognition.start();
// // }

// // // 📸 Face Recognition After Wake Word
// // async function startCameraAndRecognizeFace() {
// //   try {
// //     if (!video) {
// //       console.error("❌ Video element not found in DOM.");
// //       botStatus.innerText = "Face recognition error: Camera element missing.";
// //       return;
// //     }

// //     const stream = await navigator.mediaDevices.getUserMedia({ video: true });
// //     video.srcObject = stream;

// //     await new Promise(resolve => setTimeout(resolve, 2000));

// //     canvas.width = video.videoWidth;
// //     canvas.height = video.videoHeight;
// //     const ctx = canvas.getContext("2d");
// //     ctx.drawImage(video, 0, 0);

// //     stream.getTracks().forEach(track => track.stop());

// //     const blob = await new Promise(resolve => canvas.toBlob(resolve, "image/jpeg"));
// //     const formData = new FormData();
// //     formData.append("file", blob, "snapshot.jpg");

// //     const res = await fetch("/recognize-face", {
// //       method: "POST",
// //       body: formData,
// //     });

// //     const data = await res.json();

// //     if (data.success && data.name) {
// //       botStatus.innerText = `✅ Welcome ${data.name}`;
// //       const audio = new Audio("data:audio/mp3;base64," + data.audio_base64);
// //       audio.play();
// //       setTimeout(() => {
// //         window.location.href = `/chat?name=${encodeURIComponent(data.name)}`;
// //       }, 3000);
// //     } else {
// //       botStatus.innerText = "❌ Face not recognized. Say 'Hi SIA' again.";
// //     }

// //   } catch (err) {
// //     console.error("❌ Face recognition failed:", err);
// //     botStatus.innerText = "Face recognition error.";
// //   }
// // }
// // // //working // // //
// let slideIndex = 0;
// const slides = document.getElementsByClassName("slide");
// const botAvatar = document.getElementById("bot-avatar");
// const botStatus = document.getElementById("bot-status");
// const siaOutput = document.getElementById("sia-output");
// const video = document.getElementById("video");
// const canvas = document.getElementById("canvas");

// // 🔄 Auto slideshow
// function showSlides() {
//   for (let slide of slides) {
//     slide.style.display = "none";
//   }

//   slideIndex = (slideIndex + 1) % slides.length;
//   slides[slideIndex].style.display = "block";

//   const isLastSlide = slideIndex === slides.length - 1;

//   botAvatar.src = isLastSlide
//     ? "/static/registration_qr.png"
//     : "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnZ2ZjN2N3Z1d3pqaHloaXdmaG9qcmhkNXo1NW5ldmxmMGdpaXlwNSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/VDMHgvx8N9U7UUlczQ/giphy.gif";

//   const delay = isLastSlide ? 8000 : 3000;
//   setTimeout(showSlides, delay);
// }

// showSlides();

// // 🎙️ Wake word setup
// const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

// if (!SpeechRecognition) {
//   alert("Your browser does not support Speech Recognition. Please use Google Chrome.");
// } else {
//   const recognition = new SpeechRecognition();
//   recognition.continuous = true;
//   recognition.lang = 'en-US';
//   recognition.interimResults = false;

//   recognition.onstart = () => {
//     console.log("🎤 Voice recognition started");
//     siaOutput.innerText = "🎤 Listening...";
//   };

//   recognition.onresult = async (event) => {
//     const transcript = event.results[event.results.length - 1][0].transcript.trim().toLowerCase();
//     console.log("🗣️ Heard:", transcript);
//     siaOutput.innerText = `You said: "${transcript}"`;

//     const triggers = ["hi sia", "hello sia", "hey sia", "ok sia","hello", "start sia", "siya", "sia", "hi siya", "hello siya", "hey siya", "ok siya", "start siya"];
//     if (triggers.some(trigger => transcript.includes(trigger))) {
//       botStatus.innerText = "🟢 Wake word detected. Recognizing face...";
//       await startCameraAndRecognizeFace();
//     }
//   };

//   recognition.onerror = (e) => {
//     console.error("❌ Recognition error:", e);
//     siaOutput.innerText = "Error: " + e.error;
//   };

//   recognition.onend = () => {
//     console.warn("🔁 Restarting recognition...");
//     recognition.start();
//   };

//   recognition.start();
// }

// // 📸 Face recognition logic
// async function startCameraAndRecognizeFace() {
//   try {
//     if (!video) {
//       console.error("❌ Video element not found.");
//       botStatus.innerText = "Camera error: element missing.";
//       return;
//     }

//     const stream = await navigator.mediaDevices.getUserMedia({ video: true });
//     video.srcObject = stream;

//     await new Promise(resolve => setTimeout(resolve, 2000));

//     canvas.width = video.videoWidth;
//     canvas.height = video.videoHeight;
//     const ctx = canvas.getContext("2d");
//     ctx.drawImage(video, 0, 0);

//     stream.getTracks().forEach(track => track.stop());

//     const blob = await new Promise(resolve => canvas.toBlob(resolve, "image/jpeg"));
//     const formData = new FormData();
//     formData.append("file", blob, "snapshot.jpg");

//     const res = await fetch("/recognize-face", {
//       method: "POST",
//       body: formData,
//     });

//     const data = await res.json();

//     if (data.success && data.name) {
//       botStatus.innerText = `✅ Welcome ${data.name}`;

//       // 🔁 Audio Greeting
//       if (data.audio_base64) {
//         const audio = new Audio("data:audio/mp3;base64," + data.audio_base64);
//         audio.play();
//       }

//       // 🎯 Redirect to greeting template if available
//       if (data.card && data.card.image_url) {
//         const query = new URLSearchParams({
//           title: data.card.event,
//           message: data.card.message,
//           image: data.card.image_url
//         });
//         setTimeout(() => {
//           window.location.href = `/template?${query.toString()}`;
//         }, 3000);
//       } else {
//         setTimeout(() => {
//           window.location.href = `/chat?name=${encodeURIComponent(data.name)}`;
//         }, 3000);
//       }

//     } else {
//       botStatus.innerText = "❌ Face not recognized. Say 'Hi SIA' again.";
//     }

//   } catch (err) {
//     console.error("❌ Face recognition failed:", err);
//     botStatus.innerText = "Face recognition error.";
//   }
// }
let slideIndex = 0;
const slides = document.getElementsByClassName("slide");
const botAvatar = document.getElementById("bot-avatar");
const botStatus = document.getElementById("bot-status");
const siaOutput = document.getElementById("sia-output");
const video = document.getElementById("video");
const canvas = document.getElementById("canvas");

// 🔁 Slideshow
function showSlides() {
  for (let slide of slides) {
    slide.style.display = "none";
  }

  slideIndex = (slideIndex + 1) % slides.length;
  slides[slideIndex].style.display = "block";

  const isLastSlide = slideIndex === slides.length - 1;
  botAvatar.src = isLastSlide
    ? "/static/registration_qr.png"
    : "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnZ2ZjN2N3Z1d3pqaHloaXdmaG9qcmhkNXo1NW5ldmxmMGdpaXlwNSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/VDMHgvx8N9U7UUlczQ/giphy.gif";

  const delay = isLastSlide ? 8000 : 3000;
  setTimeout(showSlides, delay);
}

showSlides();

// 🎙️ Wake Word Setup
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {
  alert("Your browser does not support Speech Recognition. Please use Google Chrome.");
} else {
  const recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.lang = 'en-US';
  recognition.interimResults = false;

  recognition.onstart = () => {
    console.log("🎤 Voice recognition started");
    siaOutput.innerText = "🎤 Listening...";
  };

  recognition.onresult = async (event) => {
    const transcript = event.results[event.results.length - 1][0].transcript.trim().toLowerCase();
    console.log("🗣️ Heard:", transcript);
    siaOutput.innerText = `You said: "${transcript}"`;

    const triggers = [
      "hi sia", "hello sia", "hey sia", "ok sia", "start sia",
      "hi siya", "hello siya", "hey siya", "ok siya", "start siya",
      "sia", "siya"
    ];

    if (triggers.some(trigger => transcript.includes(trigger))) {
      botStatus.innerText = "🟢 Wake word detected. Recognizing face...";
      await startCameraAndRecognizeFace();
    }
  };

  recognition.onerror = (e) => {
    console.error("❌ Recognition error:", e);
    siaOutput.innerText = "Error: " + e.error;
  };

  recognition.onend = () => {
    console.warn("🔁 Restarting recognition...");
    recognition.start();
  };

  recognition.start();
}

// 📷 Face Recognition Logic
async function startCameraAndRecognizeFace() {
  try {
    if (!video) {
      console.error("❌ Video element not found.");
      botStatus.innerText = "Camera error: element missing.";
      return;
    }

    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    await new Promise(resolve => setTimeout(resolve, 2000));

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    stream.getTracks().forEach(track => track.stop());

    const blob = await new Promise(resolve => canvas.toBlob(resolve, "image/jpeg"));
    const formData = new FormData();
    formData.append("file", blob, "snapshot.jpg");

    const res = await fetch("/recognize-face", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    if (data.success && data.name) {
      botStatus.innerText = `✅ Welcome ${data.name}`;

      // 🔊 Audio Greeting
      if (data.audio_base64) {
        const audio = new Audio("data:audio/mp3;base64," + data.audio_base64);
        audio.play();
      }

      // 🧭 Redirection
      if (data.redirect_url) {
        // Redirect to template page if card info is present
        setTimeout(() => {
          window.location.href = data.redirect_url;
        }, 4000);
      } else {
        // Fallback to chat page
        setTimeout(() => {
          window.location.href = `/chat?name=${encodeURIComponent(data.name)}`;
        }, 4000);
      }

    } else {
      botStatus.innerText = "❌ Face not recognized. Say 'Hi SIA' again.";
    }

  } catch (err) {
    console.error("❌ Face recognition failed:", err);
    botStatus.innerText = "Face recognition error.";
  }
}
