from neo4jdb import *
from db import *

if __name__ == '__main__':
    entries = []
    brands = []
    ingredients = []
    drug_classes = []
    driver = get_neo_connection('drugsdbuser', 'drugsdbuser')
    session = driver.session(database='drugsdb')

    delete_all(session)  # Reset all
    records = select_nodes()
    for record in records:
        brand = record[0].strip()
        ingredient = record[1].strip()
        drug_class = record[2].strip()
        brands.append(brand)
        ingredients.append(ingredient)
        drug_classes.append(drug_class)

    brands = list(set(brands))
    ingredients = list(set(ingredients))
    drug_classes = list(set(drug_classes))

    # Create Ingredient Nodes
    for ingredient in ingredients:
        print('Creating Ingredient node with name = ', ingredient)
        create_node(ingredient, 'Ingredient', session)

    # Create Drug Node
    for brand in brands:
        print('Creating Brand Node with name = ', brand)
        create_node(brand, 'Drug', session)

    # Create Drug Class Node
    for drug_class in drug_classes:
        print('Creating Drug Class Node with name = ', drug_class)
        create_node(drug_class, 'DrugClass', session)

    # print('Gonna establish relationship')
    for record in records:
        brand = record[0].strip()
        ingredient = record[1].strip()
        drug_class = record[2].strip()
        print('Creating Relationship Between "', ingredient, '" and "', brand, '"')
        create_relationship('Ingredient', 'Drug', ingredient, brand, session, 'PRESENT_IN')
        print('Creating Relationship Between "', brand, '" and "', drug_class, '"')
        create_relationship('Drug', 'DrugClass', brand, drug_class, session, 'BELONGS_TO')
    driver.close()
