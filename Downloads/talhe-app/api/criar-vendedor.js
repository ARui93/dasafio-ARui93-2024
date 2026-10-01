import { createClient } from "@supabase/supabase-js";

// Esta chave é SECRETA — só existe aqui no servidor (variável de ambiente
// da Vercel), nunca no código que roda no navegador do usuário.
const supabaseAdmin = createClient(
  process.env.VITE_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

function slugify(texto) {
  return (texto || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ erro: "Método não permitido" });
  }

  try {
    const authHeader = req.headers.authorization || "";
    const token = authHeader.replace("Bearer ", "");
    if (!token) {
      return res.status(401).json({ erro: "Faça login novamente." });
    }

    // Confirma quem está chamando (precisa ser um gestor autenticado)
    const { data: userData, error: userErr } =
      await supabaseAdmin.auth.getUser(token);
    if (userErr || !userData?.user) {
      return res.status(401).json({ erro: "Sessão inválida." });
    }

    const { data: perfilGestor, error: perfilErr } = await supabaseAdmin
      .from("perfis")
      .select("papel, empresa_id")
      .eq("id", userData.user.id)
      .single();

    if (perfilErr || perfilGestor?.papel !== "gestor") {
      return res
        .status(403)
        .json({ erro: "Só o gestor pode criar vendedores." });
    }

    const { nomeVendedor, senha } = req.body;
    if (!nomeVendedor || !senha) {
      return res.status(400).json({ erro: "Preencha nome e senha." });
    }

    const { data: empresa, error: empresaErr } = await supabaseAdmin
      .from("empresas")
      .select("codigo")
      .eq("id", perfilGestor.empresa_id)
      .single();
    if (empresaErr) {
      return res.status(500).json({ erro: "Empresa não encontrada." });
    }

    const emailInterno = `${slugify(nomeVendedor)}@${slugify(
      empresa.codigo
    )}.marmorix.app`;

    const { data: novoUsuario, error: criarErr } =
      await supabaseAdmin.auth.admin.createUser({
        email: emailInterno,
        password: senha,
        email_confirm: true,
      });
    if (criarErr) {
      return res.status(400).json({ erro: criarErr.message });
    }

    const { error: perfilNovoErr } = await supabaseAdmin
      .from("perfis")
      .insert({
        id: novoUsuario.user.id,
        empresa_id: perfilGestor.empresa_id,
        nome: nomeVendedor,
        papel: "vendedor",
      });
    if (perfilNovoErr) {
      return res.status(500).json({ erro: perfilNovoErr.message });
    }

    return res.status(200).json({ ok: true });
  } catch (e) {
    return res.status(500).json({ erro: e.message || "Erro inesperado." });
  }
}
