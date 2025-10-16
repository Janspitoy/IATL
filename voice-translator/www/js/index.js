document.addEventListener('deviceready', onDeviceReady, false);

function onDeviceReady() {
  const recordBtn = document.getElementById('recordBtn');
  const statusEl = document.getElementById('status');
  const origText = document.getElementById('origText');
  const transText = document.getElementById('transText');
  const player = document.getElementById('player');

  // Визначаємо платформу
  const isCordova = typeof cordova !== 'undefined';

  recordBtn.addEventListener('click', () => {
    if (isCordova) {
      recordAudioCordova();
    } else {
      recordAudioBrowser();
    }
  });

  /////////////////////////////////
  // Android / Cordova
  /////////////////////////////////
  function recordAudioCordova() {
    navigator.device.capture.captureAudio(onSuccess, onError, { limit: 1, duration: 10 });

    function onSuccess(mediaFiles) {
      const file = mediaFiles[0];
      statusEl.textContent = '🎙️ Обробка аудіо...';
      uploadAudioCordova(file.fullPath);
    }

    function onError(error) {
      alert('Помилка запису: ' + JSON.stringify(error));
    }
  }

  function uploadAudioCordova(filePath) {
    const lang = document.getElementById('langSelect').value;
    const serverUrl = "http://192.168.1.133:8010/api/translate_audio/";

    const options = new FileUploadOptions();
    options.fileKey = "audio";
    options.fileName = filePath.substr(filePath.lastIndexOf('/') + 1);
    options.mimeType = "audio/wav";
    options.params = { target_lang: lang };

    const ft = new FileTransfer();
    ft.upload(filePath, encodeURI(serverUrl), function(r) {
      try {
        const response = JSON.parse(r.response);
        origText.textContent = response.original_text;
        transText.textContent = response.translated_text;
        statusEl.textContent = "✅ Переклад завершено";

        player.src = serverUrl + "output.mp3";
        player.play();
      } catch (e) {
        statusEl.textContent = "Помилка парсингу відповіді";
      }
    }, function(error) {
      statusEl.textContent = "❌ Помилка завантаження: " + JSON.stringify(error);
    }, options);
  }

  /////////////////////////////////
  // Браузер
  /////////////////////////////////
  let mediaRecorder, audioChunks;

  async function recordAudioBrowser() {
    statusEl.textContent = "🎙️ Чекаємо доступу до мікрофону...";
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];

      mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        await uploadAudioBrowser(audioBlob);
      };

      mediaRecorder.start();
      statusEl.textContent = "🎙️ Записую аудіо... Натисніть ще раз для зупинки";

      // Зупинка запису при повторному натисканні
      recordBtn.onclick = () => {
        mediaRecorder.stop();
        recordBtn.onclick = () => recordAudioBrowser(); // повертаємо кнопку
      };

    } catch (err) {
      console.error(err);
      alert('Помилка доступу до мікрофону: ' + err.message);
    }
  }

  async function uploadAudioBrowser(audioBlob) {
    const lang = document.getElementById('langSelect').value;
    const serverUrl = "http://192.168.1.133:8010/api/translate_audio/";

    statusEl.textContent = "🎙️ Обробка аудіо...";

    const formData = new FormData();
    formData.append('audio', audioBlob, 'record.wav');
    formData.append('target_lang', lang);

    try {
      const response = await fetch(serverUrl, {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      origText.textContent = data.original_text;
      transText.textContent = data.translated_text;
      statusEl.textContent = "✅ Переклад завершено";
    } catch (err) {
      console.error(err);
      statusEl.textContent = "❌ Помилка завантаження: " + err.message;
    }
  }
}
