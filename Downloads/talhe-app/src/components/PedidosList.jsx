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
  botao: {
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
  tabela: { width: "100%", borderCollapse: "collapse", fontSize: 13 },
  th: {
    textAlign: "left",
    padding: "8px 10px",
    borderBottom: "1.5px solid #4A555C",
    color: "#9CA6AA",
    fontSize: 11,
    textTransform: "uppercase",
  },
  td: {
    padding: "10px",
    borderBottom: "1px solid #2E383F",
    cursor: "pointer",
  },
  vazio: { color: "#6B7275", fontSize: 13, marginTop: 20 },
};

export default function PedidosList({ perfil, aoAbrirPedido, aoNovoPedido, aoSair, aoGerenciarVendedores }) {
  const [pedidos, setPedidos] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  useEffect(() => {
    carregar();
  }, []);

  const carregar = async () => {
    setCarregando(true);
    setErro("");
    const { data, error } = await supabase
      .from("pedidos")
      .select("*")
      .order("atualizado_em", { ascending: false });
    if (error) {
      setErro(error.message);
    } else {
      setPedidos(data || []);
    }
    setCarregando(false);
  };

  const abrir = async (pedido) => {
    const { data: pecas, error } = await supabase
      .from("pecas")
      .select("*")
      .eq("pedido_id", pedido.id);
    if (error) {
      setErro(error.message);
      return;
    }
    aoAbrirPedido({ ...pedido, pecas: pecas || [] });
  };

  return (
    <div style={estilos.pagina}>
      <div style={estilos.topo}>
        <div>
          <div style={{ fontSize: 18, fontWeight: 700 }}>Pedidos</div>
          <div style={{ fontSize: 11, color: "#9CA6AA" }}>
            {perfil?.papel === "gestor"
              ? "Todos os pedidos da empresa"
              : `Seus pedidos — ${perfil?.nome}`}
          </div>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          {perfil?.papel === "gestor" && (
            <button style={estilos.botaoSecundario} onClick={aoGerenciarVendedores}>
              vendedores
            </button>
          )}
          <button style={estilos.botaoSecundario} onClick={aoSair}>
            sair
          </button>
          <button style={estilos.botao} onClick={aoNovoPedido}>
            + novo pedido
          </button>
        </div>
      </div>

      {erro && <div style={{ color: "#D77", fontSize: 12 }}>{erro}</div>}

      {carregando ? (
        <div style={estilos.vazio}>Carregando...</div>
      ) : pedidos.length === 0 ? (
        <div style={estilos.vazio}>
          Nenhum pedido ainda. Clique em "+ novo pedido" pra começar.
        </div>
      ) : (
        <table style={estilos.tabela}>
          <thead>
            <tr>
              <th style={estilos.th}>Pedido</th>
              <th style={estilos.th}>Cliente</th>
              <th style={estilos.th}>Vendedor</th>
              <th style={estilos.th}>Prazo</th>
              <th style={estilos.th}>Atualizado</th>
            </tr>
          </thead>
          <tbody>
            {pedidos.map((p) => (
              <tr key={p.id} onClick={() => abrir(p)}>
                <td style={estilos.td}>{p.numero_pedido || "—"}</td>
                <td style={estilos.td}>{p.cliente || "—"}</td>
                <td style={estilos.td}>{p.vendedor_nome || "—"}</td>
                <td style={estilos.td}>{p.prazo ? `${p.prazo} dias` : "—"}</td>
                <td style={estilos.td}>
                  {p.atualizado_em
                    ? new Date(p.atualizado_em).toLocaleDateString("pt-BR")
                    : "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
