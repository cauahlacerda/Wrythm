import { Client, type Message } from "whatsapp-web.js";
import qrcode from "qrcode-terminal";
import sendMessage from "../service/messages.js";

console.log("Starting Bot...");

export const client = new Client({});



client.on("qr", (qr) => {
  console.log("QR code received, generate it in the terminal");
  qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
  try {
    console.log(`Client is ready!`);
  } catch (e) {
    console.log(`Erro no ready: ${e}`);
  }
});
client.on("authenticated", () => {
  console.log("Client is authenticated!");
});

client.on("auth_failure", (msg) => {
  console.log("Authentication failed:", msg);
});

client.on("disconnected", (reason) => {
  console.log("Client was logged out", reason);
});

client.on("loading_screen", (percent, message) => {
  console.log(`LOADING SCREEN ${percent}% ${message}`);
});

client.on("change_state", (state) => {
  console.log(`Client state changed to ${state}`);
});

client.on("message", async (message:Message) => {
    try {
        const chat = await message.getChat()

        if(!message.fromMe && !chat.isGroup) {
            const USER_PHONE = message.from.split("@")[0];
            console.log(`Message from ${USER_PHONE}: ${message.body}`);
            if (USER_PHONE === "558381461691") {
              await message.reply("Aguarde um momento, estou processando sua solicitação...");
              const result = await sendMessage(message.body);
              console.log(`Response to ${USER_PHONE}: ${result}`);
              await chat.sendMessage(result);

            }

        }


    } catch (error) {
        console.log(`Error processing message: ${error}`);
    }
});

client.initialize();