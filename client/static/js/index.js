function removeTask(id) {
  fetch("/remove-task", {
    method: "POST",
    body: JSON.stringify({ id }),
    headers: {
      "Content-Type": "application/json"
    }
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    if (data.ok) location.reload();
  });
}