from flask_login import current_user
from sqlalchemy.sql.expression import func

from apps import db
from apps.recipe.models import Recipes, Ingredients, Directions, Favorite_Lists, Favorites, Recipe_Ingredient, \
    Recipe_Direction


# GETTER

def get_recipe(recipe_id):
    return Recipes.query.filter_by(id=recipe_id).first()


def get_recipe_details(recipe_id):
    recipe = get_recipe(recipe_id)

    query = db.session.query(Recipe_Direction, Directions).join(Directions).filter(
        Recipe_Direction.recipe_id == recipe_id).all()
    directions = [elem[1] for elem in query]

    ingredients = db.session.query(Recipe_Ingredient, Ingredients).join(Ingredients).filter(
        Recipe_Ingredient.recipe_id == recipe_id).all()

    query = Favorites.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
    is_favorite = True if query else False

    favorite_list = None
    if is_favorite and query.list_id:
        favorite_list = Favorite_Lists.query.filter_by(id=query.list_id).first().name

    return {'general': recipe,
            'directions': directions,
            'ingredients': ingredients,
            'is_favorite': is_favorite,
            'favorite_list': favorite_list}


def get_recipes_random(count):
    favorites = db.session.query(Favorites.recipe_id).filter(Favorites.user_id == current_user.id)
    return Recipes.query.filter(~Recipes.id.in_(favorites)).order_by(func.random()).limit(count).all()


def get_favorite(recipe_id):
    return Favorites.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()


def get_favorite_lists():
    return Favorite_Lists.query.filter_by(user_id=current_user.id).all()


def get_favorite_list(list_id):
    return Favorite_Lists.query.filter_by(user_id=current_user.id, id=list_id).first()


def get_favorite_recipes(list_id):
    if list_id:
        favorites = db.session.query(Favorites.recipe_id).filter(Favorites.user_id == current_user.id).filter(
            Favorites.list_id == list_id)
    else:
        favorites = db.session.query(Favorites.recipe_id).filter(Favorites.user_id == current_user.id,
                                                                 Favorites.list_id.is_(None))

    return Recipes.query.filter(Recipes.id.in_(favorites)).all()


# SETTER

def create_favorite_list(name):
    favorite_list = Favorite_Lists.query.filter_by(name=name).first()

    if not favorite_list:
        favorite_list = Favorite_Lists(name=name, user_id=current_user.id)
        db.session.add(favorite_list)
        db.session.commit()


def edit_favorite_list(list_id, name):
    favorite_list = get_favorite_list(list_id)

    if name and favorite_list:
        query = Favorite_Lists.query.filter_by(name=name).first()

        if not query and favorite_list.name != name:
            favorite_list.name = name
            db.session.commit()


def delete_favorite_list(list_id):
    favorite_list = get_favorite_list(list_id)

    if favorite_list:
        favorites = Favorites.query.filter_by(list_id=favorite_list.id).all()
        for favorite in favorites:
            favorite.list_id = None

        db.session.delete(favorite_list)
        db.session.commit()


def add_favorite(recipe_id):
    favorite = get_favorite(recipe_id)

    if not favorite:
        favorite = Favorites(user_id=current_user.id, recipe_id=recipe_id)
        db.session.add(favorite)
        db.session.commit()


def remove_favorite(recipe_id):
    favorite = get_favorite(recipe_id)

    if favorite:
        db.session.delete(favorite)
        db.session.commit()


def clear_favorite_list(recipe_id):
    favorite = get_favorite(recipe_id)

    if favorite and favorite.list_id:
        favorite.list_id = None
        db.session.commit()


def change_favorite_list(recipe_id, list_id):
    favorite = get_favorite(recipe_id)
    favorite_list = get_favorite_list(list_id)

    if favorite and favorite_list and favorite.list_id != list_id:
        favorite.list_id = list_id
        db.session.commit()
