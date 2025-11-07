import AIResumerAPI from "../api/Api.js";




const sendMessage = async (message: string) => {
    try {
        const response = await AIResumerAPI.post("/msg", {
            message: message
        });
        
        console.log(response.data);
        console.log(`Response from API: ${response.data['result']}`);
        return response.data['result'];
        
    } catch (error) {
        console.error("Error sending message:", error);
        throw error;
    }

}
export default sendMessage