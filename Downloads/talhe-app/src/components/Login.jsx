import { useState } from "react";
import { supabase, emailVendedor } from "../lib/supabaseClient";

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
  abas: { display: "flex", gap: 8, marginBottom: 16 },
  aba: (ativa) => ({
    flex: 1,
    padding: "8px 0",
    textAlign: "center",
    fontSize: 12,
    fontWeight: 700,
    borderRadius: 3,
    cursor: "pointer",
    border: "1.5px solid #4A555C",
    background: ativa ? "#A85B3D" : "transparent",
    borderColor: ativa ? "#A85B3D" : "#4A555C",
    color: ativa ? "#fff" : "#9CA6AA",
  }),
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

export default function Login({ aoTrocarParaCadastro }) {
  const [aba, setAba] = useState("gestor"); // gestor | vendedor
  const [email, setEmail] = useState("");
  const [codigoEmpresa, setCodigoEmpresa] = useState("");
  const [nomeVendedor, setNomeVendedor] = useState("");
  const [senha, setSenha] = useState("");
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState("");
  const [modoRecuperar, setModoRecuperar] = useState(false);
  const [recuperarEnviado, setRecuperarEnviado] = useState(false);

  const entrar = async (e) => {
    e.preventDefault();
    setErro("");
    setCarregando(true);
    try {
      const emailFinal =
        aba === "gestor" ? email : emailVendedor(nomeVendedor, codigoEmpresa);
      const { error } = await supabase.auth.signInWithPassword({
        email: emailFinal,
        password: senha,
      });
      if (error) throw error;
    } catch (e) {
      setErro("Não consegui entrar. Confira os dados e tente de novo.");
    } finally {
      setCarregando(false);
    }
  };

  const enviarRecuperacao = async (e) => {
    e.preventDefault();
    setErro("");
    setCarregando(true);
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: window.location.origin,
    });
    setCarregando(false);
    if (error) {
      setErro(error.message);
      return;
    }
    setRecuperarEnviado(true);
  };

  if (modoRecuperar) {
    return (
      <div style={estilos.pagina}>
        <form style={estilos.caixa} onSubmit={enviarRecuperacao}>
          <div style={{ fontSize: 16, fontWeight: 700 }}>
            Recuperar senha
          </div>
          {recuperarEnviado ? (
            <div style={{ fontSize: 13, color: "#9CA6AA", marginTop: 12 }}>
              Enviamos um link pra <b>{email}</b>. Clique nele pra definir
              uma nova senha.
            </div>
          ) : (
            <>
              <div style={{ fontSize: 11, color: "#9CA6AA", marginTop: 4 }}>
                Só disponível pra login de gestor (que usa e-mail).
              </div>
              <label style={estilos.label}>Seu e-mail</label>
              <input
                type="email"
                style={estilos.input}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              {erro && <div style={estilos.erro}>{erro}</div>}
              <button style={estilos.botao} type="submit" disabled={carregando}>
                {carregando ? "enviando..." : "enviar link de recuperação"}
              </button>
            </>
          )}
          <div style={{ marginTop: 16, fontSize: 12, textAlign: "center" }}>
            <span
              style={estilos.link}
              onClick={() => {
                setModoRecuperar(false);
                setRecuperarEnviado(false);
                setErro("");
              }}
            >
              ‹ voltar pro login
            </span>
          </div>
        </form>
      </div>
    );
  }

  return (
    <div style={estilos.pagina}>
      <form style={estilos.caixa} onSubmit={entrar}>
        <div style={{ fontSize: 16, fontWeight: 700, marginBottom: 16 }}>
          Entrar no Talhe
        </div>

        <div style={estilos.abas}>
          <div style={estilos.aba(aba === "gestor")} onClick={() => setAba("gestor")}>
            gestor
          </div>
          <div style={estilos.aba(aba === "vendedor")} onClick={() => setAba("vendedor")}>
            vendedor
          </div>
        </div>

        {aba === "gestor" ? (
          <>
            <label style={estilos.label}>E-mail</label>
            <input
              type="email"
              style={estilos.input}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </>
        ) : (
          <>
            <label style={estilos.label}>Código da empresa</label>
            <input
              style={estilos.input}
              value={codigoEmpresa}
              onChange={(e) => setCodigoEmpresa(e.target.value)}
              placeholder="ex: stand-rj"
            />
            <label style={estilos.label}>Seu nome</label>
            <input
              style={estilos.input}
              value={nomeVendedor}
              onChange={(e) => setNomeVendedor(e.target.value)}
              placeholder="ex: Rui"
            />
          </>
        )}

        <label style={estilos.label}>Senha</label>
        <input
          type="password"
          style={estilos.input}
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />

        {aba === "gestor" && (
          <div style={{ marginTop: 10, fontSize: 11, textAlign: "right" }}>
            <span style={estilos.link} onClick={() => setModoRecuperar(true)}>
              esqueci minha senha
            </span>
          </div>
        )}

        {erro && <div style={estilos.erro}>{erro}</div>}

        <button style={estilos.botao} type="submit" disabled={carregando}>
          {carregando ? "entrando..." : "entrar"}
        </button>

        {aba === "gestor" && (
          <div style={{ marginTop: 16, fontSize: 12, textAlign: "center" }}>
            Ainda não tem empresa cadastrada?{" "}
            <span style={estilos.link} onClick={aoTrocarParaCadastro}>
              criar empresa
            </span>
          </div>
        )}
      </form>
    </div>
  );
}
