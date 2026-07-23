const https = require("https");

// Read input file path from command line argument
const inputPath = process.argv[2];
if (!inputPath) {
    console.error("Usage: node deepseek_bridge.js <input.json>");
    process.exit(1);
}

const fs = require("fs");
const input = JSON.parse(fs.readFileSync(inputPath, "utf8"));
const { url, apiKey, model, messages, temperature } = input;
const maxTokens = input.max_tokens || 2048;

const postData = JSON.stringify({
    model: model,
    messages: messages,
    temperature: temperature || 0.3,
    max_tokens: maxTokens,
});

const options = new URL(url);
const req = https.request(
    {
        hostname: options.hostname,
        port: 443,
        path: options.pathname,
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + apiKey,
            "Content-Length": Buffer.byteLength(postData),
        },
        timeout: 15000,
    },
    (res) => {
        let body = "";
        res.on("data", (chunk) => (body += chunk));
        res.on("end", () => {
            if (res.statusCode >= 200 && res.statusCode < 300) {
                process.stdout.write(body);
            } else {
                console.error("HTTP " + res.statusCode + ": " + body.substring(0, 200));
                process.exit(1);
            }
        });
    }
);

req.on("error", (e) => {
    console.error("Request failed: " + e.message);
    process.exit(1);
});

req.on("timeout", () => {
    req.destroy();
    console.error("Request timed out");
    process.exit(1);
});

req.write(postData);
req.end();
