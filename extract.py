import re,json

def company_name(linha):
    if "Company:" in linha:
        # pega a linha que comeca o nome da empresa
        company_with_code = linha.split("Company:")[1].strip()
        
        # tem um codigo apos o nome da empresa que preferi retirar tambem
        company = company_with_code.split('(')[0].strip()

        return company
    return None

def extract_product_info(linha):
    # padrao para identificar linhas de produtos (começam com número de linha)
    if re.match(r'^\d{2}\s+', linha.strip()):
        partes = linha.split()
        
        if len(partes) >= 10:
            # extrai informações básicas
            mercadoria = partes[0]  # nuero da linha
            codigo_company = partes[6]  # codigo da empresa
            
            # encontra o indice onde começa a descricao
            # por padrão, todos os prodututos tem um - antes da descricao
        
            desc_start = linha.find('-')
            if desc_start != -1:
                # pega toda a descicao após o primeiro '-'
                descricao = linha[desc_start + 1:].strip()
                
                # tenta encontrar o part number (PN:)
                part_number_match = re.search(r'PN:(\S+)', descricao)
                if part_number_match:
                    part_number = part_number_match.group(1) 
                # caso não tenha o pn, pega o primeiro codigo da descricao
                elif part_number_match == None:
                    descricao = descricao.split()
                    part_number = descricao[0]
                    descricao.pop(0)
                    descricao = ' '.join(descricao)

                else:
                    return None
                    
                
                # remove o part number da descrição para obter o nome limpo
                 
                if 'PN:' in part_number:
                    nome = descricao.split('PN:')[0].strip().rstrip('-').strip()
                else:
                    nome = descricao.rstrip('-').strip()
                return {
                    'mercadoria': mercadoria,
                    'nome': nome,
                    'part_number': part_number,
                    'codigo_company': codigo_company
                }
    
    return None

def extract(txt):
    company = None
    products = []
    
    for linha in txt.splitlines():
        # Company name
        if company is None:
            company = company_name(linha)
        
        # Product information\
        product_info = extract_product_info(linha)
        if product_info:
            products.append(product_info)
    
    return {
        'company': company,
        'products': products
    }

def return_Datajson(txt):
    data = extract(txt)
    
    
    result = {}
    for i, product in enumerate(data["products"], 1):
        result[f"mercadoria_{i:02d}"] = {
            "numero": product["mercadoria"],
            "nome": product["nome"],
            "part_number": product["part_number"],
            "codigo_company": product["codigo_company"]
        }
    
    return json.dumps(result, ensure_ascii=False, indent=2)

