const functions = require("@google-cloud/functions-framework");

functions.http("handler", (req, res) => {
  const payload = req.body || {};
  const raw = String(payload.cep ?? "").trim();
  const digits = raw.replace(/\D/g, "");

  if (digits.length !== 8) {
    res.status(400).json({ error: `CEP inválido: '${raw}' — esperado 8 dígitos` });
    return;
  }

  res.json({
    cep: digits,
    normalized: true,
    simulateFailure: Boolean(payload.simulateFailure),
  });
});
