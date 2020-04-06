# Saves uploaded photo file to server
def saveFile(files, filePath):
    if files == None:
        return 'Error: No files in request.'

    file = files['photo']

    if file is None:
        return 'Error: No file with type "photo".'

    if file.filename == '':
        return 'Error: File name is empty.'

    if file:        
        file.save(filePath)
        print('File saved.')

    return 'Successfully inserted record.'