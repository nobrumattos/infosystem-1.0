import tkinter as tk
from tkinter import ttk
from tkinter import ttk, Canvas
from tkinter import messagebox
import psutil
import os
import subprocess
import logging
import time
import random
from datetime import datetime
import socket  

# Configurar logging
log_dir = os.path.expanduser("~/Desktop/InfoSystem")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "monitoramento_sistema.log"),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class PerformanceMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitoramento de Sistema")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#2e2e2e')

        # Criar o canvas antes de chamar o background
        self.canvas = tk.Canvas(self.root, bg='#2e2e2e', width=600, height=600)
        self.canvas.pack(fill='both', expand=True)

        # Parâmetros da animação Matrix
        self.drops = []
        self.chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.drop_speed = 15
        self.drop_interval = 50  # tempo em milissegundos para a atualização
        self.drop_width = 20  # espaço entre as colunas
        self.font_size = 12

        # Adicionar background (Camada -1)
        self.add_background()

        # Criar widgets da interface (Camada 1)
        self.create_widgets()

        # Inicializar animação (Camada 0)
        self.initialize_drops()
        self.animate_matrix()

    def create_widgets(self):
        # Camada 1: Criação de botões em um frame
        main_frame = tk.Frame(self.root, bg='#2e2e2e')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Título
        title = tk.Label(main_frame, text="Escolha uma ação:", font=('Arial', 18, 'bold'), fg='#00FF00', bg='#2e2e2e')
        title.grid(row=0, column=0, columnspan=2, pady=20)

        # Adiciona um frame para os botões
        button_frame = tk.Frame(main_frame, bg='#2e2e2e')
        button_frame.grid(row=1, column=0, columnspan=2, pady=20, sticky='nsew')

        # Lista de ações e comandos
        actions = [
            ("Obter Informações do PC", self.get_system_info),
            ("Obter Últimos PIDs", self.get_recent_pids),
            ("Escanear Rede", self.scan_network),
            ("Escanear Diretórios Miscellaneous", self.scan_miscellaneous),
            ("Monitorar Desempenho", self.monitor_performance),
            ("Limpar Arquivos Gerados", self.clear_files)
        ]

        # Adiciona botões ao frame de botões
        for idx, (text, command) in enumerate(actions):
            button = tk.Button(button_frame, text=text, command=command, bg='#4a4a4a', fg='#00FF00', font=('Arial', 12))
            button.grid(row=idx, column=0, pady=10, sticky='ew')

        # Ajusta a coluna para expandir com a janela
        button_frame.columnconfigure(0, weight=1)

    def add_background(self):
        # Camada -1: Background fixo
        self.canvas.create_rectangle(0, 0, 600, 600, fill='#111111', tags='background')
        self.canvas.tag_lower('background')  # Colocar o background no nível mais baixo (-1)

    def initialize_drops(self):
        # Inicializa as posições dos drops (Camada 0)
        width = 600
        height = 600
        column_count = width // self.drop_width  # Número de colunas na tela

        # Ajustar as colunas centralmente na tela
        x_offset = (width % self.drop_width) // 2  # Para centralizar horizontalmente

        for i in range(column_count):
            x = x_offset + i * self.drop_width
            y = random.randint(-height, 0)  # Começa acima da tela
            char = random.choice(self.chars)
            self.drops.append((x, y, char))

    def animate_matrix(self):
        # Camada 0: Letras caindo (Matrix)
        self.canvas.delete('matrix')

        width = 600
        height = 600

        # Atualiza e desenha os drops
        new_drops = []
        for x, y, char in self.drops:
            self.canvas.create_text(x, y, text=char, fill='#00FF00', font=('Courier', self.font_size), tags='matrix')
            new_y = y + self.drop_speed
            if new_y < height:
                new_drops.append((x, new_y, char))
            else:
                # Reinicializa os drops que saem da tela
                new_drops.append((x, 0, random.choice(self.chars)))

        self.drops = new_drops

        # Repetir a animação
        self.root.after(self.drop_interval, self.animate_matrix)

    # Funções placeholders
    def get_system_info(self):
        pass

    def get_recent_pids(self):
        pass

    def scan_network(self):
        pass

    def scan_miscellaneous(self):
        pass

    def monitor_performance(self):
        pass

    def clear_files(self):
        pass


    def get_system_info(self):
        try:
            system_info = subprocess.getoutput('systeminfo')
            cpu_info = subprocess.getoutput('wmic cpu get caption, deviceid, name, numberofcores, numberoflogicalprocessors, maxclockspeed')

            with open(os.path.join(log_dir, "informacoes_pc.txt"), "w", encoding="utf-8") as f:
                f.write("** Informações do Sistema **\n")
                f.write(system_info + "\n\n")
                f.write("** Informações do Processador **\n")
                f.write(cpu_info)
            
            messagebox.showinfo("Concluído", "Informações do PC salvas com sucesso!")
            logging.info("Informações do PC salvas com sucesso!")
        except Exception as e:
            self.log_error_details("get_system_info", e)
            messagebox.showerror("Erro", f"Erro ao salvar informações do PC: {e}")

    def get_recent_pids(self):
        try:
            pids = psutil.pids()
            pids_info = [f"PID: {pid}, Nome: {psutil.Process(pid).name()}" for pid in pids]
            
            with open(os.path.join(log_dir, "ultimos_pids.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(pids_info))
            
            messagebox.showinfo("Concluído", "Últimos PIDs salvos com sucesso!")
            logging.info("Últimos PIDs salvos com sucesso!")
        except Exception as e:
            self.log_error_details("get_recent_pids", e)
            messagebox.showerror("Erro", f"Erro ao salvar últimos PIDs: {e}")

    def scan_network(self):
        try:
            # Listar interfaces disponíveis
            interfaces = psutil.net_if_addrs()
            if not interfaces:
                raise RuntimeError("Nenhuma interface de rede encontrada.")
            
            # Filtro de interfaces se desejado
            # interface_names = ['Ethernet', 'Wi-Fi'] # Modifique conforme necessário
            interface_names = interfaces.keys()  # Inclua todas as interfaces, se preferir

            ip_addresses = []
            for interface in interface_names:
                if interface in interfaces:
                    ip_addresses.append(f"Interface: {interface}")
                    for address in interfaces[interface]:
                        if address.family == socket.AF_INET:  # IPv4
                            ip_addresses.append(f"  - IPv4: {address.address}")
                        elif address.family == socket.AF_INET6:  # IPv6
                            ip_addresses.append(f"  - IPv6: {address.address}")
                        elif address.family == psutil.AF_LINK:  # MAC address
                            ip_addresses.append(f"  - MAC: {address.address}")

            with open(os.path.join(log_dir, "scan_rede.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(ip_addresses))
            
            messagebox.showinfo("Concluído", "Escaneamento de rede concluído com sucesso!")
            logging.info("Escaneamento de rede concluído com sucesso!")
        
        except Exception as e:
            self.log_error_details("scan_network", e)
            messagebox.showerror("Erro", f"Erro ao escanear rede: {e}")

    def scan_miscellaneous(self):
        try:
            files = []
            for root, dirs, filenames in os.walk(os.path.expanduser("~")):
                for file in filenames:
                    files.append(os.path.join(root, file))
            
            with open(os.path.join(log_dir, "arquivos_misc.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(files))
            
            messagebox.showinfo("Concluído", "Escaneamento de diretórios misc concluído com sucesso!")
            logging.info("Escaneamento de diretórios misc concluído com sucesso!")
        except Exception as e:
            self.log_error_details("scan_miscellaneous", e)
            messagebox.showerror("Erro", f"Erro ao escanear diretórios misc: {e}")

    def monitor_performance(self):
        try:
            uptime = self.get_uptime()

            # Dados de CPU, GPU e memória
            cpu_usage_samples = []
            gpu_usage_samples = []
            cpu_temp_samples = []
            memory_info = psutil.virtual_memory()
            disk_info = psutil.disk_usage('/')
            network_info = psutil.net_if_addrs()

            for _ in range(10):
                try:
                    cpu_usage_output = subprocess.getoutput('wmic cpu get loadpercentage').strip().splitlines()[1]
                    cpu_usage = int(cpu_usage_output.strip())
                    cpu_usage_samples.append(cpu_usage)
                except (IndexError, ValueError):
                    cpu_usage_samples.append(0)

                try:
                    gpu_usage_output = subprocess.getoutput('nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits').strip()
                    gpu_usage = int(gpu_usage_output)
                    gpu_usage_samples.append(gpu_usage)
                except ValueError:
                    gpu_usage_samples.append(0)

                try:
                    cpu_temp_output = subprocess.getoutput('wmic /namespace:\\\\root\\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature').strip().splitlines()[1]
                    cpu_temp = int(cpu_temp_output.strip()) / 10 - 273.15
                    cpu_temp_samples.append(cpu_temp)
                except (IndexError, ValueError):
                    pass

                time.sleep(1)

            avg_cpu_usage = sum(cpu_usage_samples) / len(cpu_usage_samples)
            avg_gpu_usage = sum(gpu_usage_samples) / len(gpu_usage_samples)
            avg_cpu_temp = sum(cpu_temp_samples) / len(cpu_temp_samples) if cpu_temp_samples else "N/A"

            mem_total = memory_info.total / (1024 ** 3)
            mem_available = memory_info.available / (1024 ** 3)
            mem_used = mem_total - mem_available
            mem_percentage = memory_info.percent

            disk_total = disk_info.total / (1024 ** 3)
            disk_used = disk_info.used / (1024 ** 3)
            disk_percentage = disk_info.percent

            with open(os.path.join(log_dir, "monitoramento_desempenho.txt"), "w", encoding="utf-8") as f:
                f.write(f"Tempo de Uptime: {uptime}\n")
                f.write(f"Uso Médio da CPU: {avg_cpu_usage:.2f}%\n")
                f.write(f"Uso Médio da GPU: {avg_gpu_usage:.2f}%\n")
                f.write(f"Temperatura Média da CPU: {avg_cpu_temp if isinstance(avg_cpu_temp, str) else f'{avg_cpu_temp:.2f}'}°C\n")
                f.write(f"Memória Total: {mem_total:.2f} GB\n")
                f.write(f"Memória Usada: {mem_used:.2f} GB ({mem_percentage:.2f}%)\n")
                f.write(f"Espaço em Disco Total: {disk_total:.2f} GB\n")
                f.write(f"Espaço em Disco Usado: {disk_used:.2f} GB ({disk_percentage:.2f}%)\n")

            messagebox.showinfo("Concluído", "Monitoramento de desempenho salvo com sucesso!")
            logging.info("Monitoramento de desempenho salvo com sucesso!")
        except Exception as e:
            self.log_error_details("monitor_performance", e)
            messagebox.showerror("Erro", f"Erro ao monitorar desempenho: {e}")

    def clear_files(self):
        try:
            files = [
                os.path.join(log_dir, "informacoes_pc.txt"),
                os.path.join(log_dir, "ultimos_pids.txt"),
                os.path.join(log_dir, "scan_rede.txt"),
                os.path.join(log_dir, "arquivos_misc.txt"),
                os.path.join(log_dir, "monitoramento_desempenho.txt")
            ]

            for file_path in files:
                if os.path.exists(file_path):
                    os.remove(file_path)

            messagebox.showinfo("Concluído", "Arquivos limpos com sucesso!")
            logging.info("Arquivos limpos com sucesso!")
        except Exception as e:
            self.log_error_details("clear_files", e)
            messagebox.showerror("Erro", f"Erro ao limpar arquivos: {e}")

    def get_uptime(self):
        try:
            uptime_seconds = time.time() - psutil.boot_time()
            days, remainder = divmod(int(uptime_seconds), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{days} dias, {hours} horas, {minutes} minutos e {seconds} segundos"
        except Exception as e:
            self.log_error_details("get_uptime", e)
            return "Não foi possível obter o uptime."

    def log_error_details(self, function_name, error):
        logging.error(f"Erro na função {function_name}: {error}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PerformanceMonitorApp(root)
    root.mainloop()
