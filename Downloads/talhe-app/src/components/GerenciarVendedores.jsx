import { useEffect, useState } from "react";
import { supabase } from "../lib/supabaseClient";

const estilos = {
  pagina: {
    minHeight: "100vh",
    background: "#1B2226",
    color: "#E7E2D5",
    fontFamily: "'IBM Plex Mono', 'Courier New', monospace",
    padding: 20,
  },
  topo: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    flexWrap: "wrap",
    gap: 12,
    marginBottom: 20,
  },
  caixa: {
    maxWidth: 380,
    background: "#242D33",
    border: "1.5px solid #4A555C",
    borderRadius: 4,
    padding: 20,
    marginBottom: 24,
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
    marginTop: 16,
    padding: "10px 14px",
    border: "1.5px solid #A85B3D",
    borderRadius: 3,
    background: "#A85B3D",
    color: "#fff",
    fontSize: 13,
    fontFamily: "inherit",
    cursor: "pointer",
    fontWeight: 700,
  },
  botaoSecundario: {
    padding: "8px 12px",
    border: "1.5px solid #4A555C",
    borderRadius: 3,
    background: "transparent",
    color: "#E7E2D5",
    fontSize: 12,
    fontFamily: "inherit",
    cursor: "pointer",
    fontWeight: 700,
  },
  linha: {
    padding: "8px 10px",
    borderBottom: "1px solid #2E383F",
    fontSize: 13,
  },
  erro: { color: "#D77", fontSize: 12, marginTop: 10 },
  ok: { color: "#8FBF8F", fontSize: 12, marginTop: 10 },
};

export default function GerenciarVendedores({ aoVoltar }) {
  const [vendedores, setVendedores] = useState([]);
  const [nome, setNome] = useState("");
  const [senha, setSenha] = useState("");
  const [carregando, setCarregando] = useState(false);
  const [msg, setMsg] = useState("");
  const [erro, setErro] = useState("");

  useEffect(() => {
    carregar();
  }, []);

  const carregar = async () => {
    const { data } = await supabase
      .from("perfis")
      .select("id, nome, criado_em")
      .eq("papel", "vendedor")
      .order("criado_em", { ascending: false });
    setVendedores(data || []);
  };

  const criarVendedor = async (e) => {
    e.preventDefault();
    setErro("");
    setMsg("");
    if (!nome || !senha) {
      setErro("Preencha nome e senha.");
      return;
    }
    setCarregando(true);
    try {
      const { data: sessao } = await supabase.auth.getSession();
      const token = sessao?.session?.access_token;
      const resp = await fetch("/api/criar-vendedor", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ nomeVendedor: nome, senha }),
      });
      const resultado = await resp.json();
      if (!resp.ok) throw new Error(resultado.erro || "Erro ao criar.");
      setMsg(`Vendedor "${nome}" criado! Já pode fazer login.`);
      setNome("");
      setSenha("");
      carregar();
    } catch (e) {
      setErro(e.message);
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div style={estilos.pagina}>
      <div style={estilos.topo}>
        <div style={{ fontSize: 18, fontWeight: 700 }}>Vendedores</div>
        <button style={estilos.botaoSecundario} onClick={aoVoltar}>
          ‹ voltar aos pedidos
        </button>
      </div>

      <form style={estilos.caixa} onSubmit={criarVendedor}>
        <div style={{ fontSize: 13, fontWeight: 700 }}>Novo vendedor</div>
        <label style={estilos.label}>Nome</label>
        <input
          style={estilos.input}
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          placeholder="ex: Rui"
        />
        <label style={estilos.label}>Senha</label>
        <input
          type="password"
          style={estilos.input}
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />
        {erro && <div style={estilos.erro}>{erro}</div>}
        {msg && <div style={estilos.ok}>{msg}</div>}
        <button style={estilos.botao} type="submit" disabled={carregando}>
          {carregando ? "criando..." : "criar vendedor"}
        </button>
      </form>

      <div style={{ fontSize: 13, fontWeight: 700, marginBottom: 8 }}>
        Vendedores cadastrados
      </div>
      {vendedores.length === 0 ? (
        <div style={{ color: "#6B7275", fontSize: 13 }}>Nenhum ainda.</div>
      ) : (
        vendedores.map((v) => (
          <div key={v.id} style={estilos.linha}>
            {v.nome}
          </div>
        ))
      )}
    </div>
  );
}
