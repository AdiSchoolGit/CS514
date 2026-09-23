document.addEventListener("submit", (event) => {
  const button = event.submitter;
  if (!button) {
    return;
  }
  button.disabled = true;
});
