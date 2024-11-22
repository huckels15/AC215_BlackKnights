export const getDEEPFOOLAlex = async (model, attack) => {
    const url = "http://34.138.29.34:8000/alexnet-attack/";
    const imageUrl =
    "http://34.138.29.34:8000/get-file/?file_path=figures/example_1_original_vs_adversarial.png";
    const payload = {
      model: model,
      attack: attack,
      max_iter: 1,
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

      const imageResponse = await fetch(imageUrl);
      if (!imageResponse.ok) {
        throw new Error(`Failed to download image. Status: ${imageResponse.status}`);
      }

      const imageBlob = await imageResponse.blob();

      const imageObjectURL = URL.createObjectURL(imageBlob);

      return {
        json: jsonResponse,
        image: imageObjectURL,
      };
    } catch (error) {
      console.error("Error fetching data:", error);
      return { error: "Failed to fetch response." };
    }
  };
  