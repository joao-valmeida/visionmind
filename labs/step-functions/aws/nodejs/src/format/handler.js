exports.handler = async (event) => {
  const v = event.viacep;
  return {
    status: "SUCCESS",
    cep: event.cep,
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
};
