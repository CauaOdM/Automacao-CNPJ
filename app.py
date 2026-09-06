import streamlit as st
import pyperclip as pclip
import pyautogui as gui
import read_cnpj.read_cnpj as rpj
from path import AgrupadorPDF
import time

timelimit = 30
breaktime= 0.2

st.title("COGNUS - Certidão de CNPJ")
st.divider()

with st.sidebar:
    st.text("Envie o arquivo Excel no campo abaixo:")

    arquivo = st.file_uploader(
        "Importe aqui",
        type=["xlsx", "xls"]
    )

    if arquivo is not None:
        try:
            with st.spinner("Processando e carregando dados..."):
                leitor = rpj.ReadExcel(arquivo)
                cnpjs = leitor.list_cnpj()

            st.success(f"{len(cnpjs)} CNPJs carregados!")

        except Exception as erro:
            st.error(f"Erro ao processar o Excel: {erro}")
    else:
        st.info("Aguardando o envio do arquivo.")

st.text("1 - Envie seu arquivo")
st.text("2 - Execute a automação e aguarde!")

st.divider()

st.subheader("Acesse o link: ")
st.link_button("Certidões","https://servicos.receitafederal.gov.br/servico/certidoes/#/home")


st.divider()

if st.button("Iniciar"):
    if arquivo is None:
        st.warning("Envie o arquivo Excel antes de iniciar.")
    elif not cnpjs:
        st.warning("Nenhum CNPJ válido foi encontrado.")
    else:
        begin = time.monotonic()
        link_found = False

        while not link_found:
            try:
                link = gui.locateCenterOnScreen(
                    "assets/link.png",
                    confidence = 0.95
                )
                gui.click(link)
                link_found = True
            except gui.ImageNotFoundException:
                if time.monotonic() - begin >= timelimit:
                    st.error("Tempo excedido: Tente Novamente")
                    st.stop()

                time.sleep(breaktime)

        begin = time.monotonic()
        pj_web = False

        while pj_web == False:
            try:
                juridica = gui.locateCenterOnScreen(
                    "assets/PJ.png",
                    confidence=0.95
                )
                gui.click(juridica)
                pj_web = True
            except gui.ImageNotFoundException:
                if time.monotonic() - begin >= timelimit:
                    st.error("Tempo excedido: Tente Novamente")
                    st.stop()

                time.sleep(breaktime)

        begin = time.monotonic()
        campo_found = False

        while not campo_found:
            try:
                campo = gui.locateCenterOnScreen(
                    "assets/campo.png",
                    confidence = 0.95
                )
                gui.click(campo)
                campo_found = True

            except gui.ImageNotFoundException:
                if time.monotonic() - begin >= timelimit:
                    st.error("Tempo excedido: Tente Novamente")
                    st.stop()

                time.sleep(breaktime)
        t = 0
        organizador = AgrupadorPDF()
        for cnpj in cnpjs:
            t+=1
            cnpj = str(cnpj).strip()

            pclip.copy(cnpj)

            gui.hotkey("ctrl", "v")
            gui.press("enter")

            if t>=len(cnpjs):
                break

            # ==========================================
            # DESCOBRE QUAL RESULTADO APARECEU
            # ==========================================

            begin = time.monotonic()
            tipo_resultado = None
            nova = None

            while tipo_resultado is None:
                try:
                    gui.locateOnScreen(
                        "assets/encontrado.png",
                        confidence=0.95
                    )

                    tipo_resultado = "existente"

                except gui.ImageNotFoundException:
                    try:
                        nova = gui.locateCenterOnScreen(
                            "assets/nova_consulta.png",
                            confidence=0.95
                        )

                        tipo_resultado = "normal"

                    except gui.ImageNotFoundException:
                        if time.monotonic() - begin >= timelimit:
                            st.error(
                                f"Tempo excedido ao processar o CNPJ {cnpj}."
                            )
                            st.stop()

                        time.sleep(breaktime)

            # ==========================================
            # CERTIDÃO JÁ EXISTENTE
            # ==========================================

            begin = time.monotonic()
            campo_found = False

            while not campo_found:
                # Primeiro verifica se a próxima tela já abriu
                try:
                    campo = gui.locateCenterOnScreen(
                        "assets/campo.png",
                        confidence=0.95
                    )

                    gui.click(campo.x, campo.y)
                    campo_found = True

                except gui.ImageNotFoundException:
                    pass

                # Se o campo ainda não apareceu, tenta clicar novamente
                try:
                    nova = gui.locateCenterOnScreen(
                        "assets/nova_consulta.png",
                        confidence=0.95
                    )

                    gui.click(nova.x, nova.y)

                except gui.ImageNotFoundException:
                    try:
                        nova2 = gui.locateCenterOnScreen(
                            "assets/nova_consulta2.png",
                            confidence=0.95
                        )

                        gui.click(nova2.x, nova2.y)

                    except gui.ImageNotFoundException:
                        pass

                if time.monotonic() - begin >= timelimit:
                    st.error(
                        f"Não foi possível iniciar a próxima consulta após o CNPJ {cnpj}."
                    )
                    st.stop()

                time.sleep(breaktime)

        st.success("Certidões geradas com sucesso!")
        pasta, quantidade_baixada, quantidade_esperada = organizador.agrupar(len(cnpjs))

        if quantidade_baixada == quantidade_esperada:
            st.success(
                f"{quantidade_baixada} certificados foram salvos em: {pasta}"
            )
        else:
            st.warning(
                f"Esperados: {quantidade_esperada}. "
                f"Encontrados: {quantidade_baixada}. "
                f"Pasta: {pasta}"
            )