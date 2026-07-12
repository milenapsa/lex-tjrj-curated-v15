import os
PORT=int(os.getenv("PORT","8080"))
UPSTREAM=os.getenv("LEX_UPSTREAM","http://homosapiens-lex-tjmg-curated-v14:8080")
VERSION="0.15.2-tjrj-curated"
UA="Lex-HomoSapiens/0.15.2"
TTL=1800
SUMULAS="https://portaltj.tjrj.jus.br/documents/d/portal-conhecimento/sumulas-2026"
CANCELADAS="https://portaltj.tjrj.jus.br/documents/d/portal-conhecimento/sumulas-canceladas"
PORTAL="https://www.tjrj.jus.br/jurisprudencia"
