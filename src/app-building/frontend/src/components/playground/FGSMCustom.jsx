export const uploadFile = async (file, type) => {
    const url = type === "model" ? "http://34.138.29.34:8000/upload-model/" : "http://34.138.29.34:8000/upload-dataset/";
  
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      const response = await fetch(url, {
        method: "POST",
        body: formData,
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      const jsonResponse = await response.json();
      return jsonResponse;
    } catch (error) {
      console.error("Error uploading file:", error);
      return { error: "Failed to upload file." };
    }
  };
  
  export const getFGSMCustom = async (model, attack, epsilon) => {
    const url = "http://34.138.29.34:8000/predict/";
  
    const payload = {
      instances: [
        {
          model: model, // Assumes the model file name is uploaded
          attack: attack,
          epsilon: epsilon,
        },
      ],
    };
  
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      const jsonResponse = await response.json();
      return jsonResponse;
    } catch (error) {
      console.error("Error fetching prediction:", error);
      return { error: "Failed to fetch prediction." };
    }
  };
  