export const getDEEPFOOLcustom = async (model, attack, additionalValues) => {
    const frontendUrl = `${window.location.protocol}//${window.location.hostname}`;
    // Replace frontend port (3000) with backend port (3001)
    const backendBaseUrl = `${frontendUrl}:3001`;
    const url = `${backendBaseUrl}/api/predict`;
    const payload = {
      "endpointId": "187542598838124544",
      "location": "us-central1",
      instances: [
        {
          model: model,
          model_path: "gs://custom-attacks-multi/run/test_example.h5",
          data_path: "gs://custom-attacks-multi/run/data",
          width: 28,
          height: 28,
          channels: 1,
          attack: attack,
          max_iter: additionalValues.maxIterations || 1,
        },
      ],
    };
  
    try {
      // Send the request to the backend
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
  
      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }
  
      const jsonResponse = await response.json();
  
      // Extract and process response data
      const base64Image = jsonResponse.predictions[0]?.figure;
      const regAcc = jsonResponse.predictions[0]?.reg_acc;
      const advAcc = jsonResponse.predictions[0]?.adv_acc;
  
      // Convert base64 image to object URL for rendering
      const decodedImage = base64Image
        ? `data:image/png;base64,${base64Image}`
        : null;
  
      return {
        decodedImage,
        regAcc,
        advAcc,
      };
    } catch (error) {
      console.error("Error fetching data:", error);
      return { error: "Failed to fetch response or process data." };
    }
  };
  