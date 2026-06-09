const { app } = require("@azure/functions");
const df = require("durable-functions");

app.http("cepHttp", {
  route: "cep",
  methods: ["POST"],
  authLevel: "function",
  extraInputs: [df.input.durableClient()],
  handler: async (request, context) => {
    const client = df.getClient(context);
    let body;
    try {
      body = await request.json();
    } catch {
      return { status: 400, body: "Invalid JSON" };
    }
    const instanceId = await client.startNew("cepOrchestrator", { input: body });
    return client.createCheckStatusResponse(request, instanceId);
  },
});
