export const getPGDRes = async (model, attack) => {
    const url = "http://34.57.140.84:8000/resnet-attack/";
    const payload = {
      model: model,
      attack: attack,
      epsilon: 0.2, // Default epsilon value, you can modify as needed
      eps_step: 0.01, // Default step value, you can modify as needed
      max_iter: 10, // Default iteration value, you can modify as needed
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
      console.error("Error fetching data:", error);
      return { error: "Failed to fetch response." };
    }
  };
  