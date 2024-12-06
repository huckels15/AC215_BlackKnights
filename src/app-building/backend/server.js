const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const fetch = (...args) => import("node-fetch").then(({ default: fetch }) => fetch(...args));
const { GoogleAuth } = require("google-auth-library");

const app = express();
const PORT = 3001;

// Middleware
app.use(cors()); // Allow all origins
app.use(bodyParser.json());

// Replace with your GCP project details
const PROJECT_ID = "secret-cipher-399620";

// API to fetch the external IP of the VM
app.get("/api/external-ip", async (req, res) => {
  try {
    const ipResponse = await fetch(
      "http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip",
      { headers: { "Metadata-Flavor": "Google" } }
    );
    const vmIp = await ipResponse.text();
    res.json({ ip: vmIp });
  } catch (error) {
    console.error("Error fetching VM IP:", error.message);
    res.status(500).json({ error: "Failed to retrieve VM IP" });
  }
});

// API to handle prediction requests
app.post("/api/predict", async (req, res) => {
  try {
    const { endpointId, location, instances } = req.body;

    if (!endpointId || !location || !instances) {
      return res.status(400).json({ error: "Missing required fields: endpointId, location, or instances" });
    }

    // Authenticate with Google Cloud
    const auth = new GoogleAuth();
    const client = await auth.getClient();
    const tokenResponse = await client.getAccessToken();
    const token = tokenResponse.token || tokenResponse;
    console.log("Generated Token:", token);

    // Construct the Vertex AI endpoint URL dynamically based on location
    const url = `https://${location}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${location}/endpoints/${endpointId}:predict`;

    // Forward the request to the Vertex AI API
    const response = await fetch(url, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ instances }),
    });

    // Handle Vertex AI API response
    if (!response.ok) {
      const errorText = await response.text();
      console.error("Error from Vertex AI:", errorText);
      return res.status(response.status).send(errorText);
    }

    const data = await response.json();
    res.json(data);
  } catch (err) {
    console.error("Backend Error:", err.message);
    res.status(500).send({ error: err.message });
  }
});

// Start the server
app.listen(PORT, "0.0.0.0", () => {
  console.log(`Backend server running on http://0.0.0.0:${PORT}`);
});
