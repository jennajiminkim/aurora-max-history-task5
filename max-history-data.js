/* T05 AI A — pure data model for the AURORA MAX HISTORY handoff.
 * Read-only transformation. Never touches browser storage, NOAA fetch, or event archive.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.MaxHistoryData = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  function safeNumber(v) {
    if (v === null || v === undefined || v === '') return null;
    const n = Number(v);
    return Number.isFinite(n) ? n : null;
  }
  function peakOf(row) {
    const knownMax = safeNumber(row?.max_value);
    const latest = safeNumber(row?.normalized_value);
    return knownMax !== null ? knownMax : latest;
  }
  function sourceTimeForMax(row) {
    if (!row) return null;
    const s = row.max_source_time || row.source_time || null;
    return typeof s === 'string' && !Number.isNaN(Date.parse(s)) ? s : null;
  }
  function utcLabel(value) {
    if (!value || Number.isNaN(Date.parse(value))) return '--';
    return new Date(value).toISOString().slice(0, 16).replace('T', ' ') + ' UTC';
  }
  function model(records) {
    const byDate = new Map();
    for (const r of (Array.isArray(records) ? records : [])) {
      if (!r || !/^\d{4}-\d{2}-\d{2}$/.test(r.record_date || '')) continue;
      const latest = safeNumber(r.normalized_value);
      const maximum = peakOf(r);
      if (latest === null || maximum === null) continue;
      const previous = byDate.get(r.record_date);
      if (previous && String(previous.fetchedAt || '') > String(r.fetched_at || '')) continue;
      byDate.set(r.record_date, {
        date: r.record_date,
        latest,
        max: maximum,
        maxTime: sourceTimeForMax(r),
        maxTimeLabel: utcLabel(sourceTimeForMax(r)),
        unit: r.unit || 'pt',
        fetchedAt: r.fetched_at || null,
        legacyFallback: safeNumber(r.max_value) === null
      });
    }
    const rows = [...byDate.values()].sort((a,b) => b.date.localeCompare(a.date));
    const highest = rows.reduce((best, cur) => !best || cur.max > best.max || (cur.max === best.max && cur.date > best.date) ? cur : best, null);
    return { rows, highest, count: rows.length };
  }
  function addTestReading(records, reading) {
    // In-memory model for H08 only; never write a browser's real live keys.
    const array = [...(records || [])];
    const date = reading.record_date;
    const idx = array.findIndex(r => r.record_date === date);
    const previous = idx >= 0 ? array[idx] : null;
    const max = previous && peakOf(previous) > Number(reading.normalized_value) ? peakOf(previous) : Number(reading.normalized_value);
    const maxTime = previous && peakOf(previous) > Number(reading.normalized_value) ? sourceTimeForMax(previous) : reading.source_time;
    const row = {...reading,max_value:max,max_source_time:maxTime};
    if (idx >= 0) array[idx] = row; else array.push(row);
    return array;
  }
  return Object.freeze({safeNumber,peakOf,sourceTimeForMax,utcLabel,model,addTestReading});
});
