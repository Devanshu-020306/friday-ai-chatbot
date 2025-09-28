async function sendMessage() {
  const input = document.getElementById("message");
  const chatbox = document.getElementById("chatbox");
  const lang = document.getElementById("lang").value;

  const message = input.value.trim();
  if (!message) return;

  chatbox.innerHTML += `<div class="user"><b>You:</b> ${message}</div>`;

  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: message, lang: lang })
  });

  const data = await response.json();

  chatbox.innerHTML += `<div class="bot"><b>Bot:</b> ${data.response}</div>`;

  // Speak reply
  const utterance = new SpeechSynthesisUtterance();
  utterance.text = data.response.replace(/<[^>]*>/g, ""); // remove HTML tags

  // Language mapping for browser TTS
  if (lang === "hi" || lang === "raj") {
    utterance.lang = "hi-IN";  // Hindi voice for Hindi + Rajasthani
  } else if (lang === "bn") {
    utterance.lang = "bn-IN";
  } else if (lang === "mr") {
    utterance.lang = "mr-IN";
  } else if (lang === "ta") {
    utterance.lang = "ta-IN";
  } else if (lang === "te") {
    utterance.lang = "te-IN";
  } else if (lang === "gu") {
    utterance.lang = "gu-IN";
  } else if (lang === "pa") {
    utterance.lang = "pa-IN";
  } else if (lang === "kn") {
    utterance.lang = "kn-IN";
  } else if (lang === "ml") {
    utterance.lang = "ml-IN";
  } else if (lang === "or") {
    utterance.lang = "or-IN";
  } else {
    utterance.lang = "en-US";  // fallback to English
  }

  // Pick a matching available voice
  const voices = window.speechSynthesis.getVoices();
  const voice = voices.find(v => v.lang === utterance.lang);
  if (voice) utterance.voice = voice;

  window.speechSynthesis.speak(utterance);

  input.value = "";
  chatbox.scrollTop = chatbox.scrollHeight;
}