import { useState } from "react";
import { supabase } from "../lib/supabaseClient";

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

export default function NovaSenha({ aoConcluir }) {
  const [senha, setSenha] = useState("");
  const [confirmar, setConfirmar] = useState("");
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState("");

  const salvar = async (e) => {
    e.preventDefault();
    setErro("");
    if (senha.length < 6) {
      setErro("A senha precisa ter pelo menos 6 caracteres.");
      return;
    }
    if (senha !== confirmar) {
      setErro("As senhas não conferem.");
      return;
    }
    setCarregando(true);
    const { error } = await supabase.auth.updateUser({ password: senha });
    setCarregando(false);
    if (error) {
      setErro(error.message);
      return;
    }
    aoConcluir();
  };

  return (
    <div style={estilos.pagina}>
      <form style={estilos.caixa} onSubmit={salvar}>
        <div style={{ fontSize: 16, fontWeight: 700 }}>Definir nova senha</div>

        <label style={estilos.label}>Nova senha</label>
        <input
          type="password"
          style={estilos.input}
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />

        <label style={estilos.label}>Confirmar senha</label>
        <input
          type="password"
          style={estilos.input}
          value={confirmar}
          onChange={(e) => setConfirmar(e.target.value)}
        />

        {erro && <div style={estilos.erro}>{erro}</div>}

        <button style={estilos.botao} type="submit" disabled={carregando}>
          {carregando ? "salvando..." : "salvar nova senha"}
        </button>
      </form>
    </div>
  );
}
