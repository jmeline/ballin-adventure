## Wallbase configuration ##
#
category= 'toplist'
pageNum = str(0)
board = '213'
res_opt = 'eqeq'
res = '0x0'
aspect = '0'
purity = '100'
thmpp = '60'
sort = '1d'

fileLayout = [category, sort, purity]

def buildUrl():
     return 'http://wallbase.cc/%s/%s?section=wallpapers&q=&res_opt=%s&res=%s&thpp=%s&purity=%s&board=%s&aspect=%s&ts=%s' % \
        (category, pageNum, res_opt, res, thmpp, purity, board, aspect, sort)
    
def updateUrl(pageNum=0):

    page = str(pageNum)
    return 'http://wallbase.cc/%s/%s?section=wallpapers&q=&res_opt=%s&res=%s&thpp=%s&purity=%s&board=%s&aspect=%s&ts=%s' % \
        (category, page, res_opt, res, thmpp, purity, board, aspect, sort)
        
def returnThmpp():
    return thmpp

def returnFileLayout():
    return fileLayout
