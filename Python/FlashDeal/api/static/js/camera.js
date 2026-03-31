/**
 * camera.js — Bildförhandsvisning vid uppladdning av erbjudandebild
 * Används på sidan "Nytt erbjudande" i butikspanelen
 */

(function () {
  const input   = document.getElementById('photo-input');
  const preview = document.getElementById('photo-preview');
  const box     = document.getElementById('photo-upload-box');
  const label   = document.getElementById('photo-label');

  if (!input || !preview) return;

  input.addEventListener('change', function () {
    const file = this.files[0];
    if (!file) return;

    // Kolla filstorlek (max 5 MB)
    if (file.size > 5 * 1024 * 1024) {
      alert('Bilden är för stor (max 5 MB).');
      this.value = '';
      return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
      preview.src     = e.target.result;
      preview.style.display = 'block';
      if (label) label.style.display = 'none';
    };
    reader.readAsDataURL(file);
  });

  // Dra-och-släpp-stöd
  if (box) {
    box.addEventListener('dragover', e => { e.preventDefault(); box.style.borderColor = 'var(--accent)'; });
    box.addEventListener('dragleave', () => { box.style.borderColor = ''; });
    box.addEventListener('drop', e => {
      e.preventDefault();
      box.style.borderColor = '';
      const file = e.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) {
        const dt = new DataTransfer();
        dt.items.add(file);
        input.files = dt.files;
        input.dispatchEvent(new Event('change'));
      }
    });
  }
})();

/**
 * Förhandsgranskning av erbjudandekortet i realtid (på "Nytt erbjudande"-sidan)
 */
(function () {
  function bind(fieldId, targetId, transform) {
    const field  = document.getElementById(fieldId);
    const target = document.getElementById(targetId);
    if (!field || !target) return;
    field.addEventListener('input', () => {
      target.textContent = transform ? transform(field.value) : field.value;
    });
  }

  bind('title',          'preview-title');
  bind('description',    'preview-desc');
  bind('deal_price',     'preview-price', v => v ? v + ' kr' : '— kr');
  bind('original_price', 'preview-orig',  v => v ? v + ' kr' : '');
  bind('quantity',       'preview-qty',   v => v ? v + ' st' : '');

  const durSelect = document.getElementById('duration_hours');
  const durLabel  = document.getElementById('preview-expires');
  if (durSelect && durLabel) {
    durSelect.addEventListener('change', () => {
      const h   = parseInt(durSelect.value) || 3;
      const now = new Date();
      now.setHours(now.getHours() + h);
      durLabel.textContent = now.toLocaleTimeString('sv-SE', { hour: '2-digit', minute: '2-digit' }) + ' idag';
    });
  }
})();
