import os
import ast
import sqlite3
import pandas as pd

DATA_PATH = "./data"
DATABASE_PATH = "./frontend/apps/db.sqlite3"


def process_element(elem):
    # Convert to string, strip, delete quotes
    elem = str(elem)
    elem = elem.strip()
    elem = elem.replace("\"", "")
    return elem


def process_df(df, columns):
    for column in columns:
        # Process elements with above function
        df[column] = df[column].apply(process_element)
    return df


def explode_df(df, columns):
    for column in columns:
        # Convert list-like column to literal-type and explode it
        df[column] = df[column].apply(ast.literal_eval)
        df = df.explode(column)
    return df


def create_files():
    full_dataset_path = os.path.join(DATA_PATH, "full-dataset.csv")
    test_dataset_path = os.path.join(DATA_PATH, "test-dataset.csv")
    import_dataset_path = os.path.join(DATA_PATH, "import-dataset.csv")

    # Load full-dataset and create a smaller version of it
    full_df = pd.read_csv(full_dataset_path, index_col=0)
    test_df = full_df.head(1000)
    test_df.to_csv(test_dataset_path, index=None)

    print(f"Size of full-dataset: {full_df.index.size}")
    print(f"Size of test-dataset: {test_df.index.size}")

    # Prepare dataset for import
    import_df = test_df
    import_df.drop("source", axis=1, inplace=True)
    import_df.drop("NER", axis=1, inplace=True)
    import_df = explode_df(import_df, ("ingredients", "directions"))
    import_df = process_df(import_df, ("title", "link", "ingredients", "directions"))
    import_df.to_csv(import_dataset_path, index=None)

    print(f"Size of import-dataset: {import_df.index.size}")


def import_data():
    path = os.path.join(DATA_PATH, "import-dataset.csv")
    df = pd.read_csv(path, index_col=None)
    print("Loaded dataset!")

    db = sqlite3.connect(DATABASE_PATH)
    cur = db.cursor()
    total_changes = 0
    print("Database connected!")

    sql_select_one = 'SELECT * FROM {} WHERE {} = {};'
    sql_select_two = 'SELECT * FROM {} WHERE {} = {} AND {} = {};'
    sql_insert = 'INSERT INTO {} ({}) VALUES ({});'
    sql_count = 'SELECT COUNT(*) FROM {} WHERE {} = {};'

    for index, row in df.iterrows():
        # --- RECIPE ---
        recipe_name = row["title"]
        recipe = cur.execute(sql_select_one.format("recipe", "name", f"\"{recipe_name}\"")).fetchone()

        if recipe:
            # print(f"Found recipe '{recipe_name}' with ID '{recipe[0]}'")
            pass
        else:
            cur.execute(sql_insert.format("recipe", "name, link", f"\"{recipe_name}\", \"{row['link']}\""))
            total_changes += cur.rowcount
            recipe = cur.execute(sql_select_one.format("recipe", "name", f"\"{recipe_name}\"")).fetchone()
            print(f"Created new recipe '{recipe_name}' with ID '{recipe[0]}'")

        recipe_id = recipe[0]

        # --- DIRECTION ---
        direction_description = row["directions"]
        direction = cur.execute(
            sql_select_one.format("direction", "description", f"\"{direction_description}\"")).fetchone()

        if direction:
            # print(f"Found direction '{direction_description}' with ID '{direction[0]}'")
            pass
        else:
            cur.execute(sql_insert.format("direction", "description", f"\"{direction_description}\""))
            total_changes += cur.rowcount
            direction = cur.execute(
                sql_select_one.format("direction", "description", f"\"{direction_description}\"")).fetchone()
            print(f"Created new direction '{direction_description}' with ID '{direction[0]}'")

        direction_id = direction[0]

        # --- INGREDIENT ---
        ingredient_name = row["ingredients"]
        ingredient = cur.execute(
            sql_select_one.format("ingredient", "name", f"\"{ingredient_name}\"")).fetchone()

        if ingredient:
            # print(f"Found ingredient '{ingredient_name}' with ID '{ingredient[0]}'")
            pass
        else:
            cur.execute(sql_insert.format("ingredient", "name", f"\"{ingredient_name}\""))
            total_changes += cur.rowcount
            ingredient = cur.execute(
                sql_select_one.format("ingredient", "name", f"\"{ingredient_name}\"")).fetchone()
            print(f"Created new ingredient '{ingredient_name}' with ID '{ingredient[0]}'")

        ingredient_id = ingredient[0]

        # --- RECIPE-DIRECTION ---
        query = cur.execute(sql_select_two.format("recipe_direction", "recipe_id", str(recipe_id), "direction_id",
                                                  str(direction_id))).fetchone()
        position = cur.execute(sql_count.format("recipe_direction", "recipe_id", str(recipe_id))).fetchone()[0]

        if query:
            # print(f"Found recipe_direction for recipe '{recipe_id}', direction '{direction_id} and position '{position}'")
            pass
        else:
            position += 1
            cur.execute(
                sql_insert.format("recipe_direction", "recipe_id, direction_id, position",
                                  f"{recipe_id}, {direction_id}, {position}"))
            total_changes += cur.rowcount
            print(
                f"Created new recipe_direction for recipe '{recipe_id}', direction '{direction_id} and position '{position}''")

        # --- RECIPE-INGREDIENT ---
        query = cur.execute(sql_select_two.format("recipe_ingredient", "recipe_id", str(recipe_id), "ingredient_id",
                                                  str(ingredient_id))).fetchone()

        if query:
            # print(f"Found recipe-ingredient for recipe '{recipe_id}' and ingredient '{ingredient_id}'")
            pass
        else:
            cur.execute(
                sql_insert.format("recipe_ingredient", "recipe_id, ingredient_id", f"{recipe_id}, {ingredient_id}"))
            total_changes += cur.rowcount
            print(f"Created new recipe-ingredient for recipe '{recipe_id}' and ingredient '{ingredient_id}'")

        db.commit()
    print(30 * "-")
    print(f"Total rows changed: {total_changes}")

    cur.close()
    db.close()
    print("Database disconnected!")


def print_duplicates():
    path = os.path.join(DATA_PATH, "test-dataset.csv")
    df = pd.read_csv(path, index_col=None)
    duplicated_df = df[df.duplicated(keep=False)]
    print(duplicated_df)


if __name__ == "__main__":
    # create_files()
    # print_duplicates()
    import_data()
