import os
import re
import yaml 
import shutil

project_root_folder = os.getcwd().replace('src', '')
artwork_src_yaml = os.path.join(project_root_folder, 'docs', '_data', 'artwork.yaml')
artwork_src_dir_model = os.path.join(os.getcwd(), 'model')
artwork_src_file_model = os.path.join(artwork_src_dir_model, 'artwork-product.html')

artwork_folder_resin = os.path.join(project_root_folder, 'docs', 'resin-artwork')
artwork_folder_tapestry = os.path.join(project_root_folder, 'docs', 'wall-tapestry')

_rex_replace_keys = re.compile('.*(REGEX_(.*?)_REGEX).*')

art_map = [
    { 'folder': artwork_folder_resin, 'index': 'index-model-resin.html' },
    { 'folder': artwork_folder_tapestry, 'index': 'index-model-tapestry.html' }
]

for art in art_map:
    print(art, art.get('folder'))

    if os.path.exists(art.get('folder')):
        shutil.rmtree(art.get('folder'), ignore_errors=True)
        
    os.makedirs(art.get('folder'))

    index_page_destination = os.path.join(art.get('folder'), 'index.html')
    index_page_model_src = os.path.join(artwork_src_dir_model, art.get('index'))
    shutil.copy(index_page_model_src, index_page_destination)

artwork_list = None

with open(artwork_src_yaml, encoding='utf8') as file:
    artwork_list = yaml.load(file, Loader=yaml.FullLoader)

for item, row in artwork_list.items():
    for product in row:
        if product.get('familly') is None:
            continue

        path = product['path']
        product["product_id"] = product['id']
        product["head_title"] = product['title']
        product["head_description"] = product['short_description']
 
        work_folder = artwork_folder_resin 
        if product['familly'] == 'tapestry':
            work_folder = artwork_folder_tapestry

        artwork_file_product_destination = os.path.join(work_folder, '%s.html' % path)

        print('artwork_file_product_destination:: ', artwork_file_product_destination)

        with open(artwork_src_file_model, 'r', encoding="utf-8") as srcfile, open(artwork_file_product_destination, 'w', encoding="utf-8") as destinationFile:
            for line in srcfile:
                updated_line = line
                
                search_keys = re.search(_rex_replace_keys, line)
                if search_keys:
                    regex_key = search_keys.group(1)
                    get_reg = search_keys.group(0)
                    product_key = search_keys.group(2).lower()

                    if product[product_key]:
                        product_key_data = product[product_key]

                        if product_key in ["head_description"]:
                            clean_html = re.compile(r'<.*?>|[^\w\s.,]')
                            cleaned_data = " ".join(product_key_data.split())
                            product_key_data = clean_html.sub('', cleaned_data)
                        
                        updated_line = line.replace(regex_key, product_key_data)

                destinationFile.write(updated_line)
            destinationFile.close()
