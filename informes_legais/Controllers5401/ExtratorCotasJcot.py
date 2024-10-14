import os
from JCOTSERVICE import RelPosicaoFundoCotistaService, ListFundosService
from .mongodbt import client
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class ExtratorCotas():
    '''extrator de cotas para o 5401 ,
    os cadastros são feitos com base no que está cadastrado , no o2'''

    service_cotas = RelPosicaoFundoCotistaService("thiago", "tAman1993**")
    cotas_colection = client['posicoes_o2_5401']['cotas']

    fundos = client['posicoes_o2_5401']['ativos_o2'].find({})
    codigos_a_buscar_cotas = pd.DataFrame.from_dict(fundos).to_dict("records")

    def __init__(self, data):
        '''a data precisa ser no formato datetime'''
        self.data = data
        self.resultado = []

    def buscar_cota(self, fundo):
        vlr_cota = self.service_cotas.get_valor_cota(fundo)
        try:
            return vlr_cota
        except Exception as e:
            print (e)
            return 0

    def job_buscar_cotas(self, fundo):
        try:
            print(fundo)
            vlr_cota = self.service_cotas.get_valor_cota(fundo)
            fundo['vlr_cota'] = vlr_cota
            self.resultado.append(fundo)
        except Exception as e:
            print (e)

    def df_cotas(self):

        list_fundos = ListFundosService(os.getenv("JCOT_USER"), os.getenv("JCOT_PASSWORD"))
        df_fundos = list_fundos.listFundoRequest()
        cotas_a_buscar = [{"codigo": item['codigo'], "dataPosicao": self.data.strftime("%Y-%m-%d")}
                          for item in df_fundos.to_dict("records")]

        with ThreadPoolExecutor(max_workers=6) as executor:
            executor.map(self.job_buscar_cotas, cotas_a_buscar)

        df_final = pd.DataFrame.from_dict(self.resultado)
        df_final['dataPosicao'] = df_final['dataPosicao'].apply(
            lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%d/%m/%Y"))
        df_final.columns = ['Ativo', "Data", "Valor"]
        df_retorno = df_final[df_final['Valor'] != ""]
        df_retorno['Valor'] = df_retorno['Valor'].apply(float)
        return df_retorno[['Data', "Ativo", "Valor"]]

    def extrair_cotas(self):
        cotas_a_buscar = [{"codigo": item['cd_jcot'], "dataPosicao": self.data.strftime("%Y-%m-%d")}
                          for item in self.codigos_a_buscar_cotas if item['cd_jcot'] != "Sem Código"]

        for fundo in cotas_a_buscar:
            cota = self.service_cotas.get_valor_cota(fundo)
            documento = {"codigo_jcot": fundo['codigo'], 'cota': cota, "data": self.data.strftime("%Y-%m-%d")}
            print(documento)
            self.cotas_colection.insert_one(documento)

    def busca_cota(self, cd_jcot, data_strftime):
        cotas_colection = client['posicoes_o2_5401']['cotas']
        try:
            return float(cotas_colection.find_one({"codigo_jcot": cd_jcot, "data": data_strftime})['cota'])
        except:
            return 1


