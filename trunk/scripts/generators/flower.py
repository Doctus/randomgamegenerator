import random

def getFlower():
    flower = ["Acacia","Acanthus","Aconite","Agrimony","Aloe","Almond","Amaranth","Amaryllis","Ambrosia","Anemone","Angrec","Apple blossom","Arborvitae","Arbutus","Arum","Asparagus","Asphodel","Aster","Azalea","Baby's breath","Bachelor button","Balm","Balsam","Balsamine","Bay wreath","Begonia","Bellflower","Bells of Ireland","Bird's-foot Trefoil","Bird-of-Paradise","Box","Broom","Bulrush","Bumblebee Orchid","Buttercup","Cabbage","Camellia japonica","Campanula","Canterbury Bells","Carnation","Celandine","Cherry","Chestnut","China aster","Chrysanthemum","Coreopsis","Cowslip","Clover","Coriander","Cypress","Daffodil","Dahlia","Daisy","Dandelion","Delphinium","Eglantine Rose","Elderflower","Fennel","Forget-me-not","Fungus","Gardenia","Geranium","Gorse","Grass","Heliotrope","Hibiscus","Hollyhock","Honeysuckle","Houseleek","Hydrangea","Iris","Ivy","Jonquil","Laurestine","Lavender","Lemon","Lettuce","Lichen","Lilac","Lily","Lily of the Valley","Lime","Lobelia","Lotus","Magnolia","Mallow","Marigold","Mayflower","Mignonette","Mint","Moonflower","Morning glory","Mullein","Nasturtium","Oak leaf","Oats","Olive","Orchid","Oxeye daisy","Peach","Pear","Peony","Phlox","Plum","Plumeria","Primrose","Poppy","Rose","Rosemary","Rue","Snowdrop","Straw","Sunflower","Sweetbrier","Thorn-apple","Thistle","Thyme","Tulip-tree","Tulip","Viscaria","Willow","Witch-hazel","Wheat"]
    return random.choice(flower)

def getName(args):
    return getFlower()
