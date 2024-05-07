from apps import db


class Recipes(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    link = db.Column(db.String(128))

    def __repr__(self):
        return f'Recipe: {self.id} - {self.name} - {self.link}'


class Ingredients(db.Model):
    __tablename__ = 'ingredient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return f'Ingredient: {self.id} - {self.name}'


class Directions(db.Model):
    __tablename__ = 'direction'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256))

    def __repr__(self):
        return f'Direction: {self.id} - {self.description}'


class Favorite_Lists(db.Model):
    __tablename__ = 'favorite_list'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Favorite_List: {self.id} - {self.name}'


class Favorites(db.Model):
    __tablename__ = 'favorite'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('favorite_list.id'), nullable=True)


class Recipe_Ingredient(db.Model):
    __tablename__ = 'recipe_ingredient'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    amount = db.Column(db.Float)
    unit = db.Column(db.String(64))


class Recipe_Direction(db.Model):
    __tablename__ = 'recipe_direction'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    direction_id = db.Column(db.Integer, db.ForeignKey('direction.id'), nullable=False)
    position = db.Column(db.Integer)
