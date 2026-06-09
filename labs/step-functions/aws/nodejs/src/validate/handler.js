exports.handler = async (event) => {
  const raw = String(event.cep ?? "").trim();
  const digits = raw.replace(/\D/g, "");

  if (digits.length !== 8) {
    throw new Error(`CEP inválido: '${raw}' — esperado 8 dígitos`);
  }

  return {
    cep: digits,
    normalized: true,
    simulateFailure: Boolean(event.simulateFailure),
  };
};
