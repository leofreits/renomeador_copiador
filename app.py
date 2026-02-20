import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import shutil
import re

class RenomeadorUniversal(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações de Interface
        self.title("App Renomeador do Leoleo")
        self.geometry("700x650")
        ctk.set_appearance_mode("dark")

        # --- Título ---
        self.label_titulo = ctk.CTkLabel(self, text="Organizador de Arquivos (Cópia e Ordenação) by Leo", font=("Roboto", 22, "bold"))
        self.label_titulo.pack(pady=20)

        # --- Frame de Seleção de Pastas ---
        self.frame_pastas = ctk.CTkFrame(self)
        self.frame_pastas.pack(pady=10, padx=20, fill="x")

        self.btn_origem = ctk.CTkButton(self.frame_pastas, text="Pasta Origem", command=self.escolher_origem)
        self.btn_origem.grid(row=0, column=0, padx=10, pady=10)
        self.lbl_origem = ctk.CTkLabel(self.frame_pastas, text="Selecione a fonte", text_color="gray")
        self.lbl_origem.grid(row=0, column=1, sticky="w")

        self.btn_destino = ctk.CTkButton(self.frame_pastas, text="Pasta Destino", command=self.escolher_destino)
        self.btn_destino.grid(row=1, column=0, padx=10, pady=10)
        self.lbl_destino = ctk.CTkLabel(self.frame_pastas, text="Selecione o destino", text_color="gray")
        self.lbl_destino.grid(row=1, column=1, sticky="w")

        # --- Configurações de Nome e Ordem ---
        self.entry_prefixo = ctk.CTkEntry(self, placeholder_text="Novo nome base (ex: Serie_Nome_SXXE)", width=400)
        self.entry_prefixo.pack(pady=20)

        self.label_ordem = ctk.CTkLabel(self, text="Critério de Identificação:")
        self.label_ordem.pack()
        self.menu_ordem = ctk.CTkOptionMenu(self, values=["Padrao SXXEXX (Série)", "Apenas Números", "Nome (A-Z)"], width=250)
        self.menu_ordem.pack(pady=10)

        # --- Barra de Progresso ---
        self.progress_label = ctk.CTkLabel(self, text="Pronto para processar", font=("Roboto", 12))
        self.progress_label.pack(pady=(20, 5))
        self.progress_bar = ctk.CTkProgressBar(self, width=500)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        # --- Botão de Execução ---
        self.btn_executar = ctk.CTkButton(self, text="INICIAR PROCESSO", fg_color="#2ecc71", hover_color="#27ae60", 
                                          command=self.processar, font=("Roboto", 16, "bold"), height=50)
        self.btn_executar.pack(pady=30)

        self.caminho_origem = ""
        self.caminho_destino = ""

    def escolher_origem(self):
        self.caminho_origem = filedialog.askdirectory()
        if self.caminho_origem:
            self.lbl_origem.configure(text=os.path.basename(self.caminho_origem), text_color="#3498db")

    def escolher_destino(self):
        self.caminho_destino = filedialog.askdirectory()
        if self.caminho_destino:
            self.lbl_destino.configure(text=os.path.basename(self.caminho_destino), text_color="#3498db")

    def extrair_logica(self, nome_arquivo):
        metodo = self.menu_ordem.get()
        nome_lc = nome_arquivo.lower()
        
        if metodo == "Padrao SXXEXX (Série)":
            # Regex que aceita S01E01, S01 E01, S01_E01 e 01x01
            padrao = r'[sS][\s_.-]?(\d+)[\s_.-]?[eE][\s_.-]?(\d+)|(\d+)x(\d+)'
            match = re.search(padrao, nome_lc)
            if match:
                # Prioriza grupos do SXXEXX, se não houver, pega do XXxXX
                temp = match.group(1) or match.group(3)
                ep = match.group(2) or match.group(4)
                return (int(temp), int(ep))
            
            # Fallback: procura qualquer número se o padrão falhar
            nums = re.findall(r'\d+', nome_lc)
            return (0, int(nums[0])) if nums else (999, 999)
            
        elif metodo == "Apenas Números":
            nums = re.findall(r'\d+', nome_lc)
            return (0, int(nums[0])) if nums else (0, 0)
            
        return nome_lc

    def processar(self):
        if not self.caminho_origem or not self.caminho_destino:
            messagebox.showwarning("Erro", "Selecione as pastas de origem e destino.")
            return

        prefixo = self.entry_prefixo.get()
        if not prefixo:
            messagebox.showwarning("Aviso", "Defina um nome base para os novos arquivos.")
            return

        # Listagem e Ordenação
        arquivos = [f for f in os.listdir(self.caminho_origem) if os.path.isfile(os.path.join(self.caminho_origem, f))]
        
        try:
            arquivos.sort(key=self.extrair_logica)
        except Exception:
            arquivos.sort()

        total = len(arquivos)
        if total == 0:
            messagebox.showinfo("Vazio", "Nenhum arquivo encontrado.")
            return

        # Processamento com Formatação de Número (01, 02...)
        try:
            for i, nome_arquivo in enumerate(arquivos):
                extensao = os.path.splitext(nome_arquivo)[1]
                
                # Formata o número com 2 dígitos (preenche com zero à esquerda até o 9)
                numero_formatado = f"{i+1:02d}"
                novo_nome = f"{prefixo}{numero_formatado}{extensao}"
                
                caminho_antigo = os.path.join(self.caminho_origem, nome_arquivo)
                caminho_novo = os.path.join(self.caminho_destino, novo_nome)
                
                shutil.copy2(caminho_antigo, caminho_novo)

                # Atualização Visual
                progresso = (i + 1) / total
                self.progress_bar.set(progresso)
                self.progress_label.configure(text=f"Processando: {i+1} de {total}")
                self.update_idletasks()

            messagebox.showinfo("Sucesso", f"Concluído! {total} arquivos copiados e organizados.")
            self.progress_label.configure(text="Processo finalizado com sucesso.")
            
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Falha na operação: {e}")

if __name__ == "__main__":
    app = RenomeadorUniversal()
    app.mainloop()

