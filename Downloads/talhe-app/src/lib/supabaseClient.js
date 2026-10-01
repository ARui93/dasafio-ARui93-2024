import { createClient } from "@supabase/supabase-js";

const url = import.meta.env.VITE_SUPABASE_URL;
const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!url || !anonKey) {
  // Isso aparece no console se esquecer de configurar o .env.local
  console.warn(
    "Supabase não configurado: preencha VITE_SUPABASE_URL e VITE_SUPABASE_ANON_KEY (veja GUIA-IMPLEMENTACAO.md)"
  );
}

export const supabase = createClient(url, anonKey);

// Transforma "João da Silva" em "joao-da-silva" (sem acento, sem espaço)
export function slugify(texto) {
  return (texto || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

// Monta o e-mail interno usado só pra login técnico do vendedor.
// O vendedor nunca vê nem digita esse e-mail — só nome + senha.
export function emailVendedor(nomeVendedor, codigoEmpresa) {
  return `${slugify(nomeVendedor)}@${slugify(codigoEmpresa)}.talhe.app`;
}
