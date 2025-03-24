function sendMessage() {
    let userInput = document.getElementById("userInput").value;
    if (userInput.trim() === "") return;

    let chatbox = document.getElementById("chatbox");

    // Display user message
    let userMessage = document.createElement("p");
    userMessage.className = "user-message";
    userMessage.innerText = "You: " + userInput;
    chatbox.appendChild(userMessage);

    // Send request to backend
    fetch("/predict", {
        method: "POST",
        body: JSON.stringify({ symptoms: userInput }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        let botMessage = document.createElement("p");
        botMessage.className = "bot-message";
        botMessage.innerHTML = `<strong>Possible Conditions:</strong> ${data.possible_conditions.join(", ")}`;
        chatbox.appendChild(botMessage);
    });

    // Clear input field
    document.getElementById("userInput").value = "";
}
