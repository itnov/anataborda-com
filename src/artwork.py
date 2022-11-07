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

        id = product['id']
        path = product['path']
        title = product['title']
        short_description = product['short_description']
 
        work_folder = artwork_folder_resin 
        if product['familly'] == 'tapestry':
            work_folder = artwork_folder_tapestry

        artwork_file_product_destination = os.path.join(work_folder, '%s.html' % path)

        print('artwork_file_product_destination:: ', artwork_file_product_destination)

        with open(artwork_src_file_model, 'r') as srcfile, open(artwork_file_product_destination, 'w') as destinationFile:
            for line in srcfile:
                updated_line = line
                
                if line.startswith('productID:'):
                    updated_line = 'productID: %s\n' % id
                elif line.startswith('  title: '):
                    updated_line = '  title: %s\n' % title             
                elif line.startswith('  short_description: '):
                    updated_line = '  description: %s\n' % short_description             
                elif re.search(_rex_replace_keys, line):
                    get_reg = re.search(_rex_replace_keys, line).group(0)
                    get_key = re.search(_rex_replace_keys, line).group(2).lower()
                    # print('MATCH:: ', get_reg, get_key)
                    if product[get_key]:
                        updated_line = line.replace(get_reg, product[get_key])
                        # print('MATCH and REPLACE:: ', get_reg, get_key)

                destinationFile.write(updated_line)
            destinationFile.close()
        # if not path == None:
        #     shutil.copy(destinationFile.name, work_folder)
