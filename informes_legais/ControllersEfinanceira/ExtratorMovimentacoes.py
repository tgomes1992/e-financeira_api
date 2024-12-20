import requests
import pandas as pd
from ..models import BaseMovimentacoes  , ContaEfin , ResgatesJcot , MovimentoDetalhado , AplicacoesJcot
from backup_modules.JCOTSERVICE import RelAnaliticoCotistaFundo , ConsultaMovimentoPeriodoV2Service , ListFundosService
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class ExtratorMovimentacoes():

    print (os.environ.get("JCOT_USER"),os.environ.get("JCOT_PASSWORD"))

    service_movimentos = RelAnaliticoCotistaFundo(os.environ.get("JCOT_USER"),
                                                           os.environ.get("JCOT_PASSWORD"))
    
    service_buscar_resgates = ConsultaMovimentoPeriodoV2Service(os.environ.get("JCOT_USER"),
                                                           os.environ.get("JCOT_PASSWORD"))

    def buscar_movimentos(self, dados):
        movimentos = self.service_movimentos.get_movimento_periodo_request(dados)
        return movimentos

    def buscar_movimentos_detalhados(self,dados):
        movimentos = self.service_movimentos.get_movimentos_detalhados(dados)
        for item in movimentos:
            nmovimento = MovimentoDetalhado.from_dict(item)
            nmovimento.save()
        return movimentos


    def get_nota_principal(self,nota):
        principal = 0
        notas = MovimentoDetalhado.objects.filter(notaOperacao = nota).all()

        for item in notas:
            principal +=  item.vlOriginal

        return principal


    def atualizar_principal_notas_resgate(self):
        resgates = ResgatesJcot.objects.filter(vl_original=0).all()
        print (len(resgates))
        for resgate in resgates:
            resgate.vl_original = self.get_nota_principal(resgate.nota)
            resgate.save()


    def main_extrair_movimentacoes(self ,  data_inicial , data_final):

        fundos = ListFundosService(os.environ.get("JCOT_USER"),
                                     os.environ.get("JCOT_PASSWORD")).listFundoRequest()

        fundos_dtvm = fundos[fundos['administrador'] == '36113876000191']

        print (len(fundos_dtvm.to_dict("records")) ,  "Total Fundos")

        extracao = [{
            "data_inicial": data_inicial,
            "data_final": data_final,
            "cd_fundo": item['codigo'],
            "cnpj_fundo": item['cnpj']
        }   for item in fundos_dtvm.to_dict("records")]


        with ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(self.extrair_aplicacoes, extracao)
            executor.map(self.extrair_resgates,  extracao)



    def base_movimentacoes(self, dados):
        contas = self.buscar_movimentos(dados)
        try:
            contas_efin_a_salvar = [ContaEfin(
                creditos = item['aplicacao_principal'],
                debitos = item['resgate_operacao'],
                principal = item['resgate_principal'],
                creditosmsmtitu = 0,
                debitosmsmtitu= 0,
                vlrultidia = 0,
                fundoCnpj = dados['cnpj_fundo'],
                numconta = f"{item['cd_fundo']}|{item['cd_cotista']}",
                datafinal = item['data_final']
            ) for item in contas]
            for item in contas_efin_a_salvar:
                if not ContaEfin.objects.filter(creditos = item.creditos , datafinal = item.datafinal ,
                                                debitos = item.debitos , fundoCnpj = item.fundoCnpj ,
                                                numconta = item.numconta
                                                ):
                    item.save()
        except Exception as e:
            print (e)
            pass
    
    def extrair_resgates(self, dados):
        dados['movimento'] = "R"
        resgates = self.service_buscar_resgates.get_movimento_periodo_request(dados)
        try:
            resgates_a_salvar = [ResgatesJcot(
                data_movimento = item['dtMov'],
                data_liquidacao = item['dtLiqFinanceira'],
                nota = item['nota'],
                cd_tipo = item['cdTipoMov'],
                cd_cotista = item['cotista'],
                cd_fundo  = item['cdFundo'],
                vl_original = 0,
                vl_liquido = item['vlLiquido'],
                vl_bruto = item['vlBruto']
            ) for item in resgates]

            for item in resgates_a_salvar:
                # print (item)
                item.save()
        except Exception as e:
            print (e)
            pass

    def extrair_aplicacoes(self, dados):


            try:
                dados['movimento'] = "A"
                resgates = self.service_buscar_resgates.get_movimento_periodo_request(dados)
                print(resgates)
                resgates_a_salvar = [AplicacoesJcot(
                    data_movimento=item['dtMov'],
                    data_liquidacao=item['dtLiqFinanceira'],
                    nota=item['nota'],
                    cd_tipo=item['cdTipoMov'],
                    cd_cotista=item['cotista'],
                    cd_fundo=item['cdFundo'],
                    vl_original=0,
                    vl_liquido=item['vlLiquido'],
                    vl_bruto=item['vlBruto']
                ) for item in resgates]

                for item in resgates_a_salvar:
                    # print (item)
                    item.save()
            except Exception as e:
                print(e)
                pass


















