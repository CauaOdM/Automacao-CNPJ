from pathlib import Path
from datetime import datetime
import shutil


class AgrupadorPDF:
    def __init__(self):
        self.downloads = Path.home() / "Downloads"

        self.desktop = Path.home() / "Desktop"

        # Seu Windows parece utilizar o Desktop dentro do OneDrive
        if not self.desktop.exists():
            self.desktop = Path.home() / "OneDrive" / "Desktop"

        # Fotografia dos PDFs existentes antes da automação
        self.pdfs_antes = set(self.downloads.glob("*.pdf"))

    def agrupar(self, quantidade_esperada):
        pdfs_depois = set(self.downloads.glob("*.pdf"))
        novos_pdfs = pdfs_depois - self.pdfs_antes

        horario = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        pasta_destino = self.desktop / f"Certidoes_CNPJ_{horario}"

        pasta_destino.mkdir(parents=True, exist_ok=True)

        for pdf in novos_pdfs:
            destino = pasta_destino / pdf.name
            shutil.move(str(pdf), str(destino))

        return pasta_destino, len(novos_pdfs), quantidade_esperada