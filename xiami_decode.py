import urllib2

def xiami_decode(s):
    s = s.strip()
    if not s:
        return False
    result = []
    line = int(s[0])
    rows = len(s[1:]) / line
    extra = len(s[1:]) % line
    s = s[1:]
    
    for x in xrange(extra):
        result.append(s[(rows + 1) * x:(rows + 1) * (x + 1)])
    
    for x in xrange(line - extra):
        result.append(s[(rows + 1) * extra + (rows * x):(rows + 1) * extra + (rows * x) + rows])
    
    url = ''
    
    for x in xrange(rows + 1):
        for y in xrange(line):
            try:
                url += result[y][x]
            except IndexError:
                continue
    
    url = urllib2.unquote(url)
    url = url.replace('^', '0')
    return url

if __name__ == '__main__':
    url = '7h%3.8%7%29_9t2.n1275%815tFxe1F1E5373p%it6481E1%.%2a%%%%%175m3Fm2552278EpAfiFEEF56663'
    print(xiami_decode(url))
