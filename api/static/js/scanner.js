/**
 * scanner.js — QR-skanner för butikspersonalen
 * Använder jsQR (laddat från CDN i template) + getUserMedia
 * Skickar token via POST till /butik/skanna/verifiera/<token>
 */

(function () {
  const video     = document.getElementById('scanner-video');
  const canvas    = document.getElementById('scanner-canvas');
  const resultBox = document.getElementById('scanner-result');
  const ctx       = canvas ? canvas.getContext('2d') : null;

  let scanning    = true;
  let lastToken   = null;

  if (!video || !canvas || typeof jsQR === 'undefined') {
    if (resultBox) resultBox.textContent = '⚠️ Kameran kunde inte startas.';
    return;
  }

  // Starta kameran (bakre kamera på mobil)
  navigator.mediaDevices.getUserMedia({
    video: { facingMode: { ideal: 'environment' }, width: { ideal: 1280 } }
  })
  .then(stream => {
    video.srcObject = stream;
    video.setAttribute('playsinline', true);
    video.play();
    requestAnimationFrame(tick);
  })
  .catch(err => {
    showResult(false, '⚠️ Åtkomst till kameran nekades. Kontrollera webbläsarens inställningar.');
    console.error('[Scanner] getUserMedia error:', err);
  });

  function tick() {
    if (!scanning) return;

    if (video.readyState === video.HAVE_ENOUGH_DATA) {
      canvas.height = video.videoHeight;
      canvas.width  = video.videoWidth;
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const code      = jsQR(imageData.data, imageData.width, imageData.height, {
        inversionAttempts: 'dontInvert',
      });

      if (code && code.data) {
        const token = extractToken(code.data);
        if (token && token !== lastToken) {
          lastToken = token;
          scanning  = false;
          verifyToken(token);
          return;
        }
      }
    }
    requestAnimationFrame(tick);
  }

  function extractToken(url) {
    // QR-koden innehåller URL: .../butik/skanna/verifiera/<token>
    const match = url.match(/verifiera\/([a-f0-9]{48})/);
    return match ? match[1] : null;
  }

  function verifyToken(token) {
    showResult(null, '⏳ Verifierar...');

    fetch(`/butik/skanna/verifiera/${token}`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
    })
    .then(r => r.json())
    .then(data => {
      if (data.ok) {
        const detail = data.customer
          ? `\n${data.customer}${data.title ? ' — ' + data.title : ''}`
          : '';
        showResult(true, data.msg + detail);
      } else {
        showResult(false, data.msg);
      }
      // Tillåt ny skanning efter 4 sekunder
      setTimeout(() => { scanning = true; lastToken = null; requestAnimationFrame(tick); }, 4000);
    })
    .catch(err => {
      showResult(false, '⚠️ Nätverksfel. Försök igen.');
      console.error('[Scanner] verify error:', err);
      setTimeout(() => { scanning = true; lastToken = null; requestAnimationFrame(tick); }, 3000);
    });
  }

  function showResult(ok, msg) {
    if (!resultBox) return;
    resultBox.textContent = msg;
    resultBox.className   = 'scanner-result ' + (ok === true ? 'ok' : ok === false ? 'err' : '');
  }
})();
