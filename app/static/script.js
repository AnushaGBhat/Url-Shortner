function shortenURL() {
  const originalUrl = document.getElementById("originalUrl").value;
  fetch("/shorten", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: originalUrl })
  })
    .then(response => response.json())
    .then(data => {
      if (data.short_url) {
        document.getElementById("shortUrl").textContent = data.short_url;
        document.getElementById("result").style.display = "block";
      } else {
        alert("Failed to shorten URL.");
      }
    })
    .catch(error => {
      console.error("Error:", error);
      alert("Error occurred.");
    });
}

function copyToClipboard() {
  const shortUrl = document.getElementById("shortUrl").textContent;
  navigator.clipboard.writeText(shortUrl).then(() => {
    alert("Copied to clipboard!");
    setTimeout(() => {
      location.reload(); 
    }, 1000);
  });
}
