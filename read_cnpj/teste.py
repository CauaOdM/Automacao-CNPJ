from read_cnpj import ReadExcel

leitor = ReadExcel('read_cnpj/cnpjs_modelo.xlsx')
print(leitor.list_cnpj())