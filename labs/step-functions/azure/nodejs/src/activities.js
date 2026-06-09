function validateCep(payload) {
  const raw = String(payload.cep ?? "").trim();
  const digits = raw.replace(/\D/g, "");
  if (digits.length !== 8) {
    throw new Error(`CEP inválido: '${raw}' — esperado 8 dígitos`);
  }
  return {
    cep: digits,
    normalized: true,
    simulateFailure: Boolean(payload.simulateFailure),
  };
}

async function fetchCep(payload) {
  if (payload.simulateFailure) {
    throw new Error("Falha simulada em FetchCEP");
  }
  const cep = payload.cep;
  const res = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
  const data = await res.json();
  if (data.erro) {
    throw new Error(`CEP não encontrado: ${cep}`);
  }
  return { ...payload, viacep: data };
}

function formatResponse(payload) {
  const v = payload.viacep;
  return {
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
  };
}

module.exports = { validateCep, fetchCep, formatResponse };
