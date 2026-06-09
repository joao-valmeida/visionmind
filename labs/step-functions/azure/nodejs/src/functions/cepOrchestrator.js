const df = require("durable-functions");

df.app.orchestration("cepOrchestrator", function* (context) {
  const payload = context.df.getInput();
  try {
    const validated = yield context.df.callActivity("validateCepActivity", payload);
    const fetched = yield context.df.callActivity("fetchCepActivity", validated);
    return yield context.df.callActivity("formatResponseActivity", fetched);
  } catch (err) {
    return {
      status: "FAILED",
      cep: payload?.cep ?? "",
      step: "orchestrator",
      error: String(err),
    };
  }
});
