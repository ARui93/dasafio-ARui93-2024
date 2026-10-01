import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Configuração pronta pra Vercel: serve na raiz do domínio, então base fica "/".
// Só troque para "/NOME-DO-REPO/" se for publicar no GitHub Pages em vez da Vercel
// (https://SEU-USUARIO.github.io/NOME-DO-REPO/).
export default defineConfig({
  plugins: [react()],
  base: "/",
});
