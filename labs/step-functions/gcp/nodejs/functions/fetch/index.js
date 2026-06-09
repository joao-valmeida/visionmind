const functions = require("@google-cloud/functions-framework");

functions.http("handler", async (req, res) => {
  const payload = req.body || {};

  if (payload.simulateFailure) {
    res.status(500).json({ error: "Falha simulada em FetchCEP" });
    return;
  }

  const cep = payload.cep;
  if (!cep) {
    res.status(400).json({ error: "CEP ausente" });
    return;
  }

  try {
    const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
    const data = await response.json();

    if (data.erro) {
      res.status(404).json({ error: `CEP não encontrado: ${cep}` });
      return;
    }

    res.json({ ...payload, viacep: data });
  } catch (err) {
    res.status(502).json({ error: String(err) });
  }
});
