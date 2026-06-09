exports.handler = async (event) => {
  if (event.simulateFailure) {
    throw new Error("Falha simulada em FetchCEP");
  }

  const cep = event.cep;
  const res = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
  const data = await res.json();

  if (data.erro) {
    throw new Error(`CEP não encontrado: ${cep}`);
  }

  return { ...event, viacep: data };
};
