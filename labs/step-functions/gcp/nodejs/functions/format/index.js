const functions = require("@google-cloud/functions-framework");

functions.http("handler", (req, res) => {
  const payload = req.body || {};
  const v = payload.viacep;

  if (!v) {
    res.status(400).json({ error: "viacep ausente" });
    return;
  }

  res.json({
    status: "SUCCESS",
    cep: payload.cep,
    address: {
      street: v.logradouro ?? "",
      complement: v.complemento ?? "",
      neighborhood: v.bairro ?? "",
      city: v.localidade ?? "",
      state: v.uf ?? "",
      ibge: v.ibge ?? "",
    },
    source: "viacep",
    fetchedAt: new Date().toISOString(),
  });
});
