const body = document.querySelector('#records-body');
const count = document.querySelector('#record-count');
const quest = document.querySelector('#quest-filter');
const weapon = document.querySelector('#weapon-filter');
const regulation = document.querySelector('#regulation-filter');
let records = [];

function populate(select, values) {
  for (const value of [...new Set(values)].sort()) {
    select.add(new Option(value, value));
  }
}

function showMessage(message) {
  body.replaceChildren();
  const cell = body.insertRow().insertCell();
  cell.colSpan = 8;
  cell.className = 'empty';
  cell.textContent = message;
}

function render() {
  const query = quest.value.trim().toLocaleLowerCase('ja');
  const matches = records.filter(record =>
    record.quest.toLocaleLowerCase('ja').includes(query) &&
    (!weapon.value || record.weapon === weapon.value) &&
    (!regulation.value || record.regulation === regulation.value)
  );
  count.textContent = `${matches.length}件`;
  if (!matches.length) {
    showMessage('該当する記録はまだありません。');
    return;
  }
  body.replaceChildren();
  for (const record of matches) {
    const row = body.insertRow();
    const score = Number.isFinite(record.score) ? record.score.toFixed(4) : '—';
    for (const value of [
      record.quest, [record.weapon, record.style].filter(Boolean).join(' / '),
      record.time, record.hunter, record.regulation,
      record.scoreCounted ? score + '（採用）' : score
    ]) {
      row.insertCell().textContent = value;
    }
    const proof = row.insertCell();
    if (/^https?:\/\//i.test(record.proofUrl)) {
      const link = document.createElement('a');
      link.href = record.proofUrl;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = '確認';
      proof.append(link);
    }
    row.insertCell().textContent = record.publishedAt || '';
  }
}

function enableLink(id, url, text) {
  if (!url) return;
  const link = document.querySelector(id);
  link.href = url;
  link.textContent = text;
  link.classList.remove('disabled');
  link.removeAttribute('aria-disabled');
}

const config = window.TAWIKI_CONFIG || {};
const repo = (config.githubRepository || '').replace(/\/$/, '');
enableLink('#x-submit', config.xProfile, 'Xで投稿する');
enableLink('#issue-submit', repo && `${repo}/issues/new?template=time-record.yml`, 'Issueで投稿する');
enableLink('#pr-submit', repo && `${repo}/compare`, 'Pull Requestを作成する');
for (const input of [quest, weapon, regulation]) input.addEventListener('input', render);

fetch('data/records.json')
  .then(response => response.ok ? response.json() : Promise.reject())
  .then(data => {
    records = data.records || [];
    populate(weapon, records.map(record => record.weapon));
    populate(regulation, records.map(record => record.regulation));
    render();
  })
  .catch(() => showMessage('記録を読み込めませんでした。'));
