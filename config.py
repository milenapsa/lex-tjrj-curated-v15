import os
PORT=int(os.getenv("PORT","8080"))
UPSTREAM=os.getenv("LEX_UPSTREAM","http://homosapiens-lex-tjmg-curated-v14:8080")
VERSION="0.15.1-tjrj-curated"
UA="Lex-HomoSapiens/0.15.1"
TTL=1800
SUMULAS="https://portaltj.tjrj.jus.br/web/portal-conhecimento/sumulas/s%C3%BAmulas-do-tjrj"
CANCELADAS="https://www.tjrj.jus.br/documents/5736540/6284946/sumulas-canceladas.pdf"
PORTAL="https://www.tjrj.jus.br/jurisprudencia"
