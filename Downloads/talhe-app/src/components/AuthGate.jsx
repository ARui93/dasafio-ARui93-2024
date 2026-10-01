import { useEffect, useState } from "react";
import { supabase } from "../lib/supabaseClient";
import Login from "./Login";
import Cadastro from "./Cadastro";
import CompletarCadastro from "./CompletarCadastro";
import NovaSenha from "./NovaSenha";
import PedidosList from "./PedidosList";
import PedidoEditor from "./PedidoEditor";
import GerenciarVendedores from "./GerenciarVendedores";

const estilosBloqueio = {
  pagina: {
    minHeight: "100vh",
    background: "#1B2226",
    color: "#E7E2D5",
    fontFamily: "'IBM Plex Mono', 'Courier New', monospace",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: 20,
    textAlign: "center",
  },
  caixa: {
    maxWidth: 380,
    background: "#242D33",
    border: "1.5px solid #A85B3D",
    borderRadius: 4,
    padding: 24,
  },
};

export default function AuthGate() {
  const [carregandoSessao, setCarregandoSessao] = useState(true);
  const [sessao, setSessao] = useState(null);
  const [perfil, setPerfil] = useState(null);
  const [perfilCarregado, setPerfilCarregado] = useState(false);
  const [empresa, setEmpresa] = useState(null);
  const [telaAuth, setTelaAuth] = useState("login"); // login | cadastro
  const [tela, setTela] = useState("lista"); // lista | editor | vendedores
  const [pedidoAberto, setPedidoAberto] = useState(null);
  const [emRecuperacaoSenha, setEmRecuperacaoSenha] = useState(false);

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      setSessao(data.session);
      setCarregandoSessao(false);
    });
    const { data: listener } = supabase.auth.onAuthStateChange(
      (evento, novaSessao) => {
        if (evento === "PASSWORD_RECOVERY") {
          setEmRecuperacaoSenha(true);
        }
        setSessao(novaSessao);
        setPerfil(null);
        setPerfilCarregado(false);
        setEmpresa(null);
        setTela("lista");
        setPedidoAberto(null);
      }
    );
    return () => listener.subscription.unsubscribe();
  }, []);

  useEffect(() => {
    if (!sessao) return;
    (async () => {
      const { data: perfilData } = await supabase
        .from("perfis")
        .select("*")
        .eq("id", sessao.user.id)
        .single();
      setPerfil(perfilData);
      if (perfilData) {
        const { data: empresaData } = await supabase
          .from("empresas")
          .select("*")
          .eq("id", perfilData.empresa_id)
          .single();
        setEmpresa(empresaData);
      }
      setPerfilCarregado(true);
    })();
  }, [sessao]);

  const sair = async () => {
    await supabase.auth.signOut();
  };

  if (carregandoSessao) return null;

  if (emRecuperacaoSenha) {
    return <NovaSenha aoConcluir={() => setEmRecuperacaoSenha(false)} />;
  }

  if (!sessao) {
    return telaAuth === "login" ? (
      <Login aoTrocarParaCadastro={() => setTelaAuth("cadastro")} />
    ) : (
      <Cadastro aoTrocarParaLogin={() => setTelaAuth("login")} />
    );
  }

  // sessão existe, mas perfil/empresa ainda estão carregando
  if (perfil === null && !perfilCarregado) return null;

  // sessão confirmada mas ainda não existe perfil = acabou de confirmar
  // o e-mail e falta finalizar a criação da empresa
  if (perfilCarregado && !perfil) {
    return (
      <CompletarCadastro
        aoConcluir={() => {
          setPerfil(null);
          setPerfilCarregado(false);
          setSessao({ ...sessao }); // força recarregar perfil/empresa
        }}
      />
    );
  }

  if (!empresa) return null;

  if (empresa.status_assinatura !== "ativo") {
    return (
      <div style={estilosBloqueio.pagina}>
        <div style={estilosBloqueio.caixa}>
          <div style={{ fontSize: 16, fontWeight: 700, marginBottom: 8 }}>
            Acesso temporariamente bloqueado
          </div>
          <div style={{ fontSize: 13, color: "#9CA6AA" }}>
            A assinatura de <b>{empresa.nome}</b> está com status "
            {empresa.status_assinatura}". Fale com o suporte pra regularizar.
          </div>
          <button
            onClick={sair}
            style={{
              marginTop: 16,
              padding: "8px 12px",
              border: "1.5px solid #4A555C",
              borderRadius: 3,
              background: "transparent",
              color: "#E7E2D5",
              cursor: "pointer",
            }}
          >
            sair
          </button>
        </div>
      </div>
    );
  }

  if (tela === "vendedores") {
    return <GerenciarVendedores aoVoltar={() => setTela("lista")} />;
  }

  if (tela === "editor") {
    return (
      <PedidoEditor
        pedidoInicial={pedidoAberto}
        perfil={perfil}
        onVoltar={() => {
          setTela("lista");
          setPedidoAberto(null);
        }}
      />
    );
  }

  return (
    <PedidosList
      perfil={perfil}
      aoSair={sair}
      aoNovoPedido={() => {
        setPedidoAberto(null);
        setTela("editor");
      }}
      aoAbrirPedido={(pedido) => {
        setPedidoAberto(pedido);
        setTela("editor");
      }}
      aoGerenciarVendedores={() => setTela("vendedores")}
    />
  );
}
