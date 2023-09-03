const yaml = require('js-yaml');
const fs   = require('fs');
const path = require('path');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

const headers = [
    { 'id': 'id', 'title': 'id' },
    { 'id': 'title', 'title': 'title' },
    { 'id': 'description', 'title': 'description' },
    { 'id': 'availability', 'title': 'availability' },
    { 'id': 'condition', 'title': 'condition' },
    { 'id': 'price', 'title': 'price' },
    { 'id': 'link', 'title': 'link' },
    { 'id': 'image_link', 'title': 'image_link' },
    { 'id': 'brand', 'title': 'brand' },
    { 'id': 'google_product_category', 'title': 'google_product_category' },
    { 'id': 'fb_product_category', 'title': 'fb_product_category' },
    { 'id': 'quantity_to_sell_on_facebook', 'title': 'quantity_to_sell_on_facebook' },
    { 'id': 'sale_price', 'title': 'sale_price' },
    { 'id': 'sale_price_effective_date', 'title': 'sale_price_effective_date' },
    { 'id': 'item_group_id', 'title': 'item_group_id' },
    { 'id': 'gender', 'title': 'gender' },
    { 'id': 'color', 'title': 'color' },
    { 'id': 'size', 'title': 'size' },
    { 'id': 'age_group', 'title': 'age_group' },
    { 'id': 'material', 'title': 'material' },
    { 'id': 'pattern', 'title': 'pattern' },
    { 'id': 'shipping', 'title': 'shipping' },
    { 'id': 'shipping_weight', 'title': 'shipping_weight' }
]

const dataSourceFile = path.join('..', 'docs', '_data', 'artwork.yaml')
const outputFile = path.join('..', 'docs', 'assets', 'csv', 'facebook-feed.csv')
const baseUrl = 'https://anataborda.com'

const getDescription = (product) => {
    return product.short_description.replace(/(<([^>]+)>)/gi, "");
}
const getAvailability = (product) => {
    return getStock(product) ? 'in stock' : 'out of stock'
}
const getCondition = () => "new"
const getLink = (product) => {
    let linkFamilly = 'resin-artwork'
    if (product.familly == 'tapestry') {
        linkFamilly = 'wall-tapestry'
    }
    return `${baseUrl}/${linkFamilly}/${product.path}`
}
const getImage = (product) => {
    return `${baseUrl}/${product.image}`
}
const getPrice = (product) => {
    if (product.price && product.price.GBP)
        return product.price.GBP
    return 0
}
const getStock = (product) => {
    if (product.stock && product.stock > 0)
        return product.stock
    return 0
}
const getGoogleCategory = (product) => {
    if (product.familly == 'tapestry') {
        return '500045'
    }
    return '500044'
}
const getFacebookCategory = (product) => {
    if (product.familly == 'tapestry') {
        return '1003'
    }
    return '1023'
}


const getYamlData = () => {
    try {
        const fileRead = fs.readFileSync(dataSourceFile, 'utf8');
        const yamlDoc = yaml.load(fileRead);
        return yamlDoc
    } catch (e) {
        console.log(e);
    }
}

const writeCsvData = (records, writeToFile) => {
    let csvWriter = createCsvWriter({
        path: writeToFile,
        header: headers
    });
    csvWriter.writeRecords(records)
        .then(() => {
            console.log('...Done');
        });
}

const yamlProducts = getYamlData()
console.log(yamlProducts.products.length)

const dataRecords = []
for (idx in yamlProducts.products) {
    let product = yamlProducts.products[idx]
    dataRecords.push({
        'id': product.id, 
        'title': product.title, 
        'description': getDescription(product), 
        'availability': getAvailability(product), 
        'condition': getCondition(), 
        'price': getPrice(product), 
        'link': getLink(product), 
        'image_link': getImage(product), 
        'brand': 'AnaTabordaArt', 
        'google_product_category': getGoogleCategory(product), 
        'fb_product_category': getFacebookCategory(product), 
        'quantity_to_sell_on_facebook': getStock(product), 
        'sale_price': getPrice(product), 
        'sale_price_effective_date': '', 
        'item_group_id': '', 
        'gender': '', 
        'color': '', 
        'size': '', 
        'age_group': '', 
        'material': '', 
        'pattern': '', 
        'shipping': '', 
        'shipping_weight': ''
    })
}

writeCsvData(dataRecords, outputFile)
