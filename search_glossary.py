import streamlit as st
import pymupdf
import os
import glob

def search_phrase_in_pdf(pdf_path, phrase):
    """
    Searches for a phrase in a single PDF file and returns the pages where the phrase is found.

    :param pdf_path: Path to the PDF file.
    :param phrase: Phrase to search for in the PDF.
    :return: List of page numbers where the phrase is found.
    """
    found_pages = []
    with pymupdf.open(pdf_path) as pdf_document:
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            text = page.get_text()
            if phrase.lower() in text.lower():
                found_pages.append(page_number + 1)  # Page numbers are 1-indexed
    return found_pages

def search_phrase_in_multiple_pdfs(pdf_folder, phrase):
    """
    Searches for a phrase in all PDF files in a specified folder.

    :param pdf_folder: Path to the folder containing PDF files.
    :param phrase: Phrase to search for in the PDFs.
    :return: Dictionary with PDF filenames as keys and lists of found page numbers as values.
    """
    results = {}
    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            found_pages = search_phrase_in_pdf(pdf_path, phrase)
            if found_pages:
                results[filename] = found_pages
                st.write(f'{filename} {len(found_pages)} page(s) found.')
    st.markdown('---')
    return results

def display_pdf_page(pdf_path, page_number, search_phrase):
    """
    Displays a specific page of a PDF file in Streamlit.
    pip 
    :param pdf_path: Path to the PDF file.
    :param page_number: Page number to display.
    """
    with pymupdf.open(pdf_path) as pdf_document:
        page = pdf_document.load_page(page_number - 1)
        page.add_highlight_annot(page.search_for(search_phrase))
        image = page.get_pixmap(dpi=300)
        #image_path = f"{temp_image_folder}\\{pdf_path.split('/')[-1]}_page_{page_number:03d}.png"
        #image.save(image_path)
        
        return image.tobytes()
        
        

# Streamlit UI
st.title("PDF 문구 검색기")

# pdf_folder_path = os.path.join(os.path.dirname(__file__),"data")
# pdf_folder_path = os.path.dirname(__file__)
pdf_folder_path = "."
# temp_image_folder = "H:\\gith\\whatever\\search_glossarydata
# temp = glob.glob(f"{temp_image_folder}\\*.png")

# for f in temp:
#     try:
#         os.remove(f)
#     except Exception as e:
#         print(f"Error while deleting {f}: {e}")


with st.form(key="search_form"):
    search_phrase = st.text_input("검색할 문구를 입력하세요:", "")
    submit_button = st.form_submit_button(label="검색")
    
if submit_button:
    if search_phrase:
        results = search_phrase_in_multiple_pdfs(pdf_folder_path, search_phrase)
        
        if results:
            
            tabs = st.tabs(results.keys())
            
            for tab, content in zip(tabs, results):
                
                pdf_file = f"{pdf_folder_path}\\{content}"
                pages = results[content]
                with tab:
                    for page in pages:
                        image_bytes = display_pdf_page(pdf_file, page, search_phrase)
                        st.image(image_bytes, caption=f'{content.split(".")[0]} p.{page:03d}', use_column_width=True)

        else:
            st.write("검색된 문구가 없습니다.")
    else:
        st.write("검색할 문구를 입력하세요.")
