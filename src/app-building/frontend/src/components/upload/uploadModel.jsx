export const uploadModel = async (file) => {
    const url = "http://34.74.113.119:8000/predict/";
    const formData = new FormData();
    formData.append("file", file); // Ensure the key matches the server's expected field

    try {
        const response = await fetch(url, {
            method: "POST",
            body: formData, // Do not set Content-Type manually
        });

        if (!response.ok) {
            const errorText = await response.text(); // Capture error details from the server
            throw new Error(`Failed to upload model. Status: ${response.status} - ${errorText}`);
        }

        const jsonResponse = await response.json();
        return { success: true, json: jsonResponse };
    } catch (error) {
        console.error("Error uploading model:", error);
        return { success: false, error: error.message };
    }
};