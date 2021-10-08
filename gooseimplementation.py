from goose3 import Goose
g = Goose()

def text(link):
    article = g.extract(url=link)
    return str(article.cleaned_text)
