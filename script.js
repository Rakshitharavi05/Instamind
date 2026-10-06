async function analyzeProfile() {

    const url = document.getElementById("instagramUrl").value;

    if (url.trim() === "") {
        alert("Please enter an Instagram profile URL.");
        return;
    }

    // Show loading message
    const button = document.querySelector("button");

    const originalButtonText = button.innerHTML;

    button.disabled = true;
    button.innerHTML = "🤖 Analyzing with AI...";

    // Add loading overlay
    const loadingOverlay = document.createElement("div");

    loadingOverlay.id = "loadingOverlay";

    loadingOverlay.innerHTML = `
        <div class="loading-box">
            <div class="loading-spinner"></div>

            <h2>Analyzing Profile...</h2>

            <p>
                InstaMind AI is generating business insights.
            </p>

            <div class="loading-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;

    document.body.appendChild(loadingOverlay);

    try {

        const response = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                url: url
            })
        });

        const data = await response.json();

        if (!response.ok) {

            alert(data.error || "Something went wrong.");

            return;
        }

        // Save the analysis result
        localStorage.setItem(
            "analysisResult",
            JSON.stringify(data)
        );

        // Open dashboard
        window.location.href = "dashboard.html";

    } catch (error) {

        console.error(error);

        alert(
            "Could not connect to the InstaMind AI backend. " +
            "Make sure Flask is running."
        );

    } finally {

        // Remove loading screen
        const overlay = document.getElementById("loadingOverlay");

        if (overlay) {
            overlay.remove();
        }

        // Restore button
        button.disabled = false;
        button.innerHTML = originalButtonText;
    }
}