export const getSQUARERes = async (model, attack) => {
    const url = "http://34.57.140.84:8000/resnet-attack/";
    const imageUrl =
    "http://34.57.140.84:8000/get-file/?file_path=figures/example_1_original_vs_adversarial.png";
    const payload = {
      model: model,
      attack: attack,
      epsilon: 0.2,
      max_iter: 10,
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
      console.error("Error fetching data or downloading image:", error);
      return { error: "Failed to fetch response or download image." };
    }
  };
    