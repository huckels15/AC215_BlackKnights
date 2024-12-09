export const uploadData = async (file) => {
    const url = "http://34.23.11.83:8000/predict/";
    const formData = new FormData();
    formData.append("file", file); // Ensure the key matches the server's expected field

    try {
        const response = await fetch(url, {
            method: "POST",
            body: formData, // Do not set Content-Type manually
        });

        if (!response.ok) {
            const errorText = await response.text(); // Capture error details from the server
            throw new Error(`Failed to upload dataset. Status: ${response.status} - ${errorText}`);
        }

        const jsonResponse = await response.json();
        return { success: true, json: jsonResponse };
    } catch (error) {
        console.error("Error uploading dataset:", error);
        return { success: false, error: error.message };
    }
};