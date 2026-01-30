import os
from urllib.parse import urljoin
import requests
import logging
from datetime import datetime
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ANSDownloader:
    """
    Classe responsável por baixar arquivos de demonstrações contábeis da ANS.
    """
    
    BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
    RAW_DIR = "data/raw"
    
    def __init__(self):
        self.session = requests.Session()
        os.makedirs(self.RAW_DIR, exist_ok=True)
    
    def download_all(self):
        """
        Orquestra a busca e o download dos arquivos.
        """
        targets = self.get_last_3_quarters_urls()
        
        if not targets:
            logger.error("Nenhum arquivo encontrado para baixar.")
            return

        logger.info(f"Encontrados {len(targets)} arquivos para download.")
        
        for url in targets:
            filename = url.split('/')[-1]
            save_path = os.path.join(self.RAW_DIR, filename)
            
            # Evita baixar se já existe (Idempotência - termo chique que engenheiros amam)
            if os.path.exists(save_path):
                logger.info(f"Arquivo já existe, pulando: {filename}")
                continue
            
            try:
                logger.info(f"Baixando: {filename}...")
                response = self.session.get(url, stream=True)
                response.raise_for_status()
                
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                logger.info(f"Salvo em: {save_path}")
                
            except Exception as e:
                logger.error(f"Falha ao baixar {url}: {e}")
    
    def get_last_3_quarters_urls(self) -> list[str]:
        """
        Retorna as URLs completas dos últimos arquivos disponíveis.
        """
        now = datetime.now()
        year = now.year
        
        # Busca no ano atual
        urls = self._get_quarters_from_year(year)
        
        # Se não achou 3 arquivos, volta 1 ano
        if len(urls) < 3:
            logger.info(f"Menos de 3 arquivos no ano {year}. Verificando ano anterior...")
            urls_prev = self._get_quarters_from_year(year - 1)
            # Adiciona os do ano anterior antes dos atuais
            urls = urls_prev + urls
            
        # Retorna os últimos 3 encontrados
        return urls[-3:]
    
    def _get_quarters_from_year(self, year: int) -> list[str]:
        """Método auxiliar para buscar ZIPs dentro da página de um ano."""
        url_ano = f"{self.BASE_URL}{year}/"
        try:
            logger.info(f"Buscando em: {url_ano}")
            response = self.session.get(url_ano)
            response.raise_for_status()
        except requests.HTTPError:
            logger.warning(f"Diretório do ano {year} não encontrado ou inacessível.")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
    
        urls_encontradas = []
        for a in soup.find_all('a'):
            href = a.get('href')
            if href and href.lower().endswith('.zip'):
                full_url = urljoin(url_ano, href)
                urls_encontradas.append(full_url)
                
        return urls_encontradas
    

if __name__ == "__main__":
    downloader = ANSDownloader()
    downloader.download_all()