async function sendAudioToBackend(audioBlob, language) {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.webm');
  formData.append('language', language);

  const response = await fetch('/api/process_audio', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Failed to process audio');
  }

  const data = await response.json();
  return data;
}

window.sendAudioToBackend = sendAudioToBackend;