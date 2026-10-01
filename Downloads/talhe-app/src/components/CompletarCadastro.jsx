import { useEffect, useState } from "react";
import { supabase, slugify } from "../lib/supabaseClient";
import { CHAVE_PENDENTE } from "./Cadastro";

const estilos = {
  pagina: {
    minHeight: "100vh",
    background: "#1B2226",
    color: "#E7E2D5",
    fontFamily: "'IBM Plex Mono', 'Courier New', monospace",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: 20,
  },
  caixa: {
    width: "100%",
    maxWidth: 380,
    background: "#242D33",
    border: "1.5px solid #4A555C",
    borderRadius: 4,
    padding: 24,
  },
  label: {
    display: "block",
    fontSize: 10.5,
    color: "#9CA6AA",
    marginBottom: 4,
    marginTop: 12,
    textTransform: "uppercase",
    letterSpacing: 0.5,
    fontWeight: 700,
  },
  input: {
    width: "100%",
    boxSizing: "border-box",
    padding: "8px 10px",
    border: "1.5px solid #4A555C",
    borderRadius: 2,
    fontSize: 14,
    fontFamily: "inherit",
    background: "#1B2226",
    color: "#E7E2D5",
  },
  botao: {
    width: "100%",
    marginTop: 20,
    padding: "11px 14px",
    border: "1.5px solid #A85B3D",
    borderRadius: 3,
    background: "#A85B3D",
    color: "#fff",
    fontSize: 13,
    fontFamily: "inherit",
    cursor: "pointer",
    fontWeight: 700,
  },
  erro: { color: "#D77", fontSize: 12, marginTop: 12 },
};

export default function CompletarCadastro({ aoConcluir }) {
  const [nomeEmpresa, setNomeEmpresa] = useState("");
  const [codigoEmpresa, setCodigoEmpresa] = useState("");
  const [nomeGestor, setNomeGestor] = useState("");
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState("");

  useEffect(() => {
    const pendente = localStorage.getItem(CHAVE_PENDENTE);
    if (pendente) {
      try {
        const dados = JSON.parse(pendente);
        setNomeEmpresa(dados.nomeEmpresa || "");
        setCodigoEmpresa(dados.codigoEmpresa || "");
        setNomeGestor(dados.nomeGestor || "");
      } catch {}
    }
  }, []);

  const concluir = async (e) => {
    e.preventDefault();
    setErro("");
    if (!nomeEmpresa || !codigoEmpresa || !nomeGestor) {
      setErro("Preencha todos os campos.");
      return;
    }
    setCarregando(true);
    try {
      const { data: sessao } = await supabase.auth.getSession();
      const usuarioId = sessao?.session?.user?.id;
      if (!usuarioId) throw new Error("Sessão inválida. Faça login de novo.");

      // O id é gerado aqui (e não lido de volta do banco) porque, antes de
      // existir um perfil, a regra de leitura ainda não deixa a pessoa
      // enxergar a empresa que acabou de criar.
      const empresaId = crypto.randomUUID();

      const { error: empresaErro } = await supabase
        .from("empresas")
        .insert({
          id: empresaId,
          nome: nomeEmpresa,
          codigo: slugify(codigoEmpresa),
        });
      if (empresaErro) throw empresaErro;

      const { error: perfilErro } = await supabase.from("perfis").insert({
        id: usuarioId,
        empresa_id: empresaId,
        nome: nomeGestor,
        papel: "gestor",
      });
      if (perfilErro) throw perfilErro;

      localStorage.removeItem(CHAVE_PENDENTE);
      aoConcluir();
    } catch (e) {
      setErro(e.message || "Não foi possível concluir o cadastro.");
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div style={estilos.pagina}>
      <form style={estilos.caixa} onSubmit={concluir}>
        <div style={{ fontSize: 16, fontWeight: 700 }}>
          Quase lá — finalize sua empresa
        </div>
        <div style={{ fontSize: 11, color: "#9CA6AA", marginTop: 4 }}>
          E-mail confirmado! Confirme os dados da empresa abaixo.
        </div>

        <label style={estilos.label}>Nome da empresa</label>
        <input
          style={estilos.input}
          value={nomeEmpresa}
          onChange={(e) => setNomeEmpresa(e.target.value)}
          placeholder="ex: Marmoraria Stand Ltda."
        />

        <label style={estilos.label}>Código da empresa (sem espaços)</label>
        <input
          style={estilos.input}
          value={codigoEmpresa}
          onChange={(e) => setCodigoEmpresa(e.target.value)}
          placeholder="ex: stand-rj"
        />

        <label style={estilos.label}>Seu nome</label>
        <input
          style={estilos.input}
          value={nomeGestor}
          onChange={(e) => setNomeGestor(e.target.value)}
          placeholder="ex: Rui"
        />

        {erro && <div style={estilos.erro}>{erro}</div>}

        <button style={estilos.botao} type="submit" disabled={carregando}>
          {carregando ? "criando..." : "concluir cadastro"}
        </button>
      </form>
    </div>
  );
}
