import { useState } from "react";
import { supabase } from "../lib/supabaseClient";

const CHAVE_PENDENTE = "talhe_cadastro_pendente";

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
  link: { color: "#A85B3D", cursor: "pointer", textDecoration: "underline" },
};

export default function Cadastro({ aoTrocarParaLogin }) {
  const [nomeEmpresa, setNomeEmpresa] = useState("");
  const [codigoEmpresa, setCodigoEmpresa] = useState("");
  const [nomeGestor, setNomeGestor] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState("");
  const [enviado, setEnviado] = useState(false);

  const cadastrar = async (e) => {
    e.preventDefault();
    setErro("");
    if (!nomeEmpresa || !codigoEmpresa || !nomeGestor || !email || !senha) {
      setErro("Preencha todos os campos.");
      return;
    }
    setCarregando(true);
    try {
      const { error: signUpErro } = await supabase.auth.signUp({
        email,
        password: senha,
        options: { emailRedirectTo: window.location.origin },
      });
      if (signUpErro) throw signUpErro;

      // Guarda os dados da empresa pra usar assim que o e-mail for
      // confirmado (nesse momento a pessoa ainda não está autenticada,
      // então não dá pra gravar no banco ainda).
      localStorage.setItem(
        CHAVE_PENDENTE,
        JSON.stringify({ nomeEmpresa, codigoEmpresa, nomeGestor })
      );
      setEnviado(true);
    } catch (e) {
      setErro(e.message || "Não foi possível concluir o cadastro.");
    } finally {
      setCarregando(false);
    }
  };

  if (enviado) {
    return (
      <div style={estilos.pagina}>
        <div style={estilos.caixa}>
          <div style={{ fontSize: 16, fontWeight: 700 }}>
            Confirme seu e-mail
          </div>
          <div style={{ fontSize: 13, color: "#9CA6AA", marginTop: 10 }}>
            Enviamos um link de confirmação pra <b>{email}</b>. Clique no
            link e você volta automaticamente pra cá já logado, pra
            finalizar a criação da empresa.
          </div>
          <div
            style={{ ...estilos.link, marginTop: 16, display: "inline-block" }}
            onClick={aoTrocarParaLogin}
          >
            ‹ voltar
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={estilos.pagina}>
      <form style={estilos.caixa} onSubmit={cadastrar}>
        <div style={{ fontSize: 16, fontWeight: 700 }}>Criar empresa</div>
        <div style={{ fontSize: 11, color: "#9CA6AA", marginTop: 4 }}>
          Você será o gestor desta empresa no Talhe.
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
        <div style={{ fontSize: 10, color: "#6B7275", marginTop: 4 }}>
          Seus vendedores vão usar esse código pra entrar no sistema.
        </div>

        <label style={estilos.label}>Seu nome</label>
        <input
          style={estilos.input}
          value={nomeGestor}
          onChange={(e) => setNomeGestor(e.target.value)}
          placeholder="ex: Rui"
        />

        <label style={estilos.label}>Seu e-mail</label>
        <input
          type="email"
          style={estilos.input}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <label style={estilos.label}>Senha</label>
        <input
          type="password"
          style={estilos.input}
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />

        {erro && <div style={estilos.erro}>{erro}</div>}

        <button style={estilos.botao} type="submit" disabled={carregando}>
          {carregando ? "enviando..." : "criar empresa"}
        </button>

        <div style={{ marginTop: 16, fontSize: 12, textAlign: "center" }}>
          Já tem conta?{" "}
          <span style={estilos.link} onClick={aoTrocarParaLogin}>
            entrar
          </span>
        </div>
      </form>
    </div>
  );
}

export { CHAVE_PENDENTE };
