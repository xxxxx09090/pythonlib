def rm_nullstr(stri):
    result = []
    for i in range(len(stri)):
        if stri[i] != '':
            result.append(stri[i])
    return (result)
    
