import pypdf

def is_vectoriel(fichier_pdf):
    """
    
    Arguments:
        fichier_pdf {string} -- chemin vers le fichier pdf

    Retour :
        {bool} -- True si le pdf est vectoriel, False sinon

    GitHub: Github.com/Faressofiane/Is-Vectoriel-Py

    """

    with open(fichier_pdf, 'rb') as f:
        pdf_reader = pypdf.PdfReader(f)
        contenu = ''
        for page_num in range(len(pdf_reader.pages)): 
            page = pdf_reader.pages[page_num]
            contenu += page.extract_text()

        if len(contenu) == 0:
            return True
        else:
            return False

