document.querySelectorAll('.toast').forEach(t => setTimeout(() => t.remove(), 4500));
document.querySelectorAll('form[data-confirm]').forEach(f => f.addEventListener('submit', e => { if (!confirm(f.dataset.confirm)) e.preventDefault(); }));
