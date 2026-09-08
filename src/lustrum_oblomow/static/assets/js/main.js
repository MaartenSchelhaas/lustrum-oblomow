"use strict";

/**
 * Returns the UTC offset (in minutes) that `timeZone` has at the instant
 * `utcMillis`, so a wall-clock time in that zone can be converted to a UTC
 * timestamp regardless of DST.
 */
function getTimeZoneOffsetMinutes(utcMillis, timeZone) {
  const dtf = new Intl.DateTimeFormat("en-US", {
    timeZone,
    hour12: false,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
  const parts = {};
  for (const { type, value } of dtf.formatToParts(new Date(utcMillis))) {
    parts[type] = value;
  }
  const asUTC = Date.UTC(
    +parts.year,
    +parts.month - 1,
    +parts.day,
    +parts.hour === 24 ? 0 : +parts.hour,
    +parts.minute,
    +parts.second
  );
  return (asUTC - utcMillis) / 60000;
}

/**
 * Converts a wall-clock date/time in Europe/Amsterdam to a UTC timestamp,
 * automatically applying CET (UTC+1) or CEST (UTC+2) depending on whether
 * DST is in effect on that date. This keeps the countdown correct for every
 * visitor's own timezone and survives the yearly DST switch unchanged.
 */
function amsterdamTimeToUTC(isoLocal) {
  const [datePart, timePart] = isoLocal.split("T");
  const [year, month, day] = datePart.split("-").map(Number);
  const [hour, minute, second] = timePart.split(":").map(Number);
  const utcGuess = Date.UTC(year, month - 1, day, hour, minute, second || 0);
  const offsetMinutes = getTimeZoneOffsetMinutes(utcGuess, "Europe/Amsterdam");
  return utcGuess - offsetMinutes * 60000;
}

/**
 * Countdown to the lustrum founding date.
 * Only ever writes numbers via textContent, never innerHTML.
 */
function initCountdown() {
  const root = document.querySelector("[data-countdown]");
  if (!root) return;

  const target = amsterdamTimeToUTC(root.dataset.countdown);
  const els = {
    days: root.querySelector('[data-unit="days"]'),
    hours: root.querySelector('[data-unit="hours"]'),
    minutes: root.querySelector('[data-unit="minutes"]'),
    seconds: root.querySelector('[data-unit="seconds"]'),
  };

  function tick() {
    const diff = Math.max(0, target - Date.now());
    const seconds = Math.floor(diff / 1000);

    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (els.days) els.days.textContent = String(days);
    if (els.hours) els.hours.textContent = String(hours).padStart(2, "0");
    if (els.minutes) els.minutes.textContent = String(minutes).padStart(2, "0");
    if (els.seconds) els.seconds.textContent = String(secs).padStart(2, "0");

    if (diff <= 0) clearInterval(intervalId);
  }

  tick();
  const intervalId = setInterval(tick, 1000);
}

/**
 * Accessible accordion for the FAQ page. Toggles aria-expanded and a
 * max-height transition; content is static markup already in the DOM
 * (nothing is ever injected).
 */
function initAccordion() {
  const items = document.querySelectorAll(".faq-item");

  items.forEach((item) => {
    const button = item.querySelector(".faq-question");
    const answer = item.querySelector(".faq-answer");
    if (!button || !answer) return;

    if (item.getAttribute("data-open") === "true") {
      answer.style.maxHeight = `${answer.scrollHeight}px`;
    }

    button.addEventListener("click", () => {
      const isOpen = item.getAttribute("data-open") === "true";
      const next = !isOpen;

      item.setAttribute("data-open", String(next));
      button.setAttribute("aria-expanded", String(next));
      answer.style.maxHeight = next ? `${answer.scrollHeight}px` : "0px";
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initCountdown();
  initAccordion();
});
