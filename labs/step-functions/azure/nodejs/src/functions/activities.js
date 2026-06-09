const df = require("durable-functions");
const { validateCep, fetchCep, formatResponse } = require("../activities");

df.app.activity("validateCepActivity", {
  handler: validateCep,
});

df.app.activity("fetchCepActivity", {
  handler: fetchCep,
});

df.app.activity("formatResponseActivity", {
  handler: formatResponse,
});
