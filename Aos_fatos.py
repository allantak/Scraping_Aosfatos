import scrapy
#ativar ambiente C:/Users/allan/anaconda3/Scripts/activate, conda activate Scrapy        
#Pra rodar o script tem que usar um comando
#scrapy runspider teste1.py
#exit pra sair
#scrapy shell "https://www.aosfatos.org/", torna um lugar pra vc testar os comandos
#pega as informações em tres liguagem CSS, Xpath e html so pesquisar sobre parsel é um selector=é um função pra obter dados
#mas no scrapy ja tem
#dentro do shell há comandos 
#response pra ver se ta pegando
#response.css('html') o selector seleciona tudo dentro de html, so pega a primeira 
#response.css('title').getall() #pegar todas elemento com titulo, getall() ate pra xpath serve, filtra o que especificou, tirando o selector deixando mais visivel
#response.css('title::text').get() pegar o text dentro do elemento
# response.xpath('//nav//ul//li/a[re:test(@href,"checamos")]')#//pega tudo dentro do html, pegar algo especifico um atributo tem que usar esse re:test

class mainSpider(scrapy.Spider):
    name='aos_fatos'
    start_urls = ['https://www.aosfatos.org/']

    def parse(self, response):
        #import ipdb; ipdb.set_trace()#de bugar o site, test
        link =response.xpath(
            '//nav//ul//li/a[re:test(@href,"checamos")]/@href').getall()#aqui estou especificando o que vai ser obtido de informação
        for links in link:#laço de repetição para pegar cada um dos links
            yield scrapy.Request(#scrapy.Request, request=pegar as informação 
                response.urljoin(links), #URLJOIN pegar o links(caminho) juntar com a url, pra poder acessar
                callback=self.parse_category#callback=vai retorna essas informações para o parse_categoria, usando o self pq nao foi definido a variavel 
                )

    def parse_category(self, response):#cada vez que eu acionar essa função, vai mostrar um por um os links
        #import ipdb; ipdb.set_trace()
        news=response.xpath('//a[@class="card third"]/@href').getall()#Usando Xpath /=find //=findall, pra pegar algum atributo dentro de um elemeto tem que utilizar
        for new_url in news:                                            #[@variavel = "especificação"], se quiser especificar mais um atributo tem q usar /@variavel
            yield scrapy.Request(
                response.urljoin(new_url),
                callback=self.parse_new
            )
        page=response.css('div.pagination a::attr(href)').getall()
        for pages in page:
            yield scrapy.Request(
                response.urljoin(pages),
                callback=self.parse_category
            )
        #pass #PRA RODAR o laço de repetição precisa apertar c, C=close
    
    def parse_new(self,response):
        title = response.css('article h1::text').get()#' '.join vai juntar a string com uma separação de espaço
        data=' '.join(response.css('p.publish_date::text').get().split())
        quote=response.css('article blockquote p')#se colocar getall() vai filtar e vai virar um lista 
        for quotes in quote:#laço de repetiçãos pois pra o quote vim junto com o status, pq o quote pode vim nao na ordem com o status, se fosse fazer direto
            quote_text=quotes.css('::text').get()
            status=quotes.xpath('./parent::blockquote/preceding-sibling::figure//figcaption//text()').get().replace('\r\n','')
            if status=='':
                status=quotes.xpath('./parent::blockquote/preceding-sibling::figure//figcaption//figcaption/text()').get()
            #parent=pega os elementos ao todo da sua classe(bloco) conforme a sua especificação, preceding-sibling=irmao proximo, pega a classe anterior
            yield{
                'name':title,
                'data':data,
                'quote_text':quote_text,
                'status':status,
                'url': response.url #pega as url que foi utilizadas

            }#scrapy runspider Aos_fatos.py -s HTTPCACHE_ENABLED=1 -s CLOSESPIDER_ITEEMCOUNT=500 -o nomedocsv.csv
            #utiliza isso pra nao derrubar o server, pegar um request especifico e criação de csv


        
        