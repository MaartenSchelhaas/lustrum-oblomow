"use strict";

/**
 * Countdown to the lustrum founding date.
 * Only ever writes numbers via textContent, never innerHTML.
 */
function initCountdown() {
  const root = document.querySelector("[data-countdown]");
  if (!root) return;

  const target = new Date(root.dataset.countdown).getTime();
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
