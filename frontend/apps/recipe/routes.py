from flask import render_template, redirect, request
from flask_login import login_required, current_user

from apps.recipe import blueprint
from apps.recipe.forms import CollectionForm
from apps.recipe.util import get_recipe, get_recipe_details, get_recipes_random, get_favorite_lists, get_favorite_list, \
    get_favorite_recipes
from apps.recipe.util import create_favorite_list, edit_favorite_list, delete_favorite_list, add_favorite, \
    remove_favorite, clear_favorite_list, change_favorite_list


@blueprint.route('/dashboard')
@login_required
def dashboard():
    return redirect('/dashboard/inspiration')


@blueprint.route('/dashboard/<segment>', methods=['GET', 'POST'])
@login_required
def dashboard_default(segment):
    template = None
    data = {}

    if segment == 'inspiration':
        template = 'home/dashboard.html'
        data['recipes'] = get_recipes_random(10)
    elif segment == 'favorites':
        if request.method == "POST":
            action = request.form['action']
            recipe_id = action.split('_')[-1]

            if action.startswith('remove_favorite_'):
                remove_favorite(recipe_id)
            elif action.startswith('change_list_'):
                list_id = action.split('_')[-2]
                change_favorite_list(recipe_id, list_id)

        template = 'recipe/favorites.html'
        data['recipes'] = get_favorite_recipes(None)
    elif segment == 'collections':
        if request.method == "POST":
            action = request.form['action']

            if action == 'create_list':
                create_favorite_list('Untitled collection')
            elif action.startswith('edit_list_'):
                list_id = action.split('_')[-1]
                name = request.form['name']
                edit_favorite_list(list_id, name)
            elif action.startswith('delete_list_'):
                list_id = action.split('_')[-1]
                delete_favorite_list(list_id)

        template = 'recipe/collections.html'
        data['form'] = CollectionForm(request.form)

    if template:
        return render_template(template,
                               segment=segment,
                               user_id=current_user.id,
                               favorite_lists=get_favorite_lists(),
                               **data)
    else:
        return render_template('error/page-404.html'), 404


@blueprint.route('/dashboard/detail/<recipe_id>', methods=['GET', 'POST'])
@login_required
def dashboard_detail(recipe_id):
    recipe = get_recipe(recipe_id)

    if recipe:
        if request.method == "POST":
            action = request.form['action']

            if action == 'add_favorite':
                add_favorite(recipe_id)
            elif action == 'remove_favorite':
                remove_favorite(recipe_id)
            elif action == 'clear_list':
                clear_favorite_list(recipe_id)
            elif action.startswith('change_list_'):
                list_id = action.split('_')[-1]
                change_favorite_list(recipe_id, list_id)

        return render_template('recipe/detail.html',
                               segment='',
                               user_id=current_user.id,
                               favorite_lists=get_favorite_lists(),
                               recipe=get_recipe_details(recipe_id))
    else:
        return render_template('error/page-404.html'), 404


@blueprint.route('/dashboard/favorite-list/<list_id>', methods=['GET', 'POST'])
@login_required
def dashboard_favorite_list(list_id):
    current_list = get_favorite_list(list_id)

    if current_list:
        if request.method == "POST":
            action = request.form['action']
            recipe_id = action.split('_')[-1]

            if action.startswith('remove_favorite_'):
                remove_favorite(recipe_id)
            elif action.startswith('clear_list_'):
                clear_favorite_list(recipe_id)
            elif action.startswith('change_list_'):
                new_list_id = action.split('_')[-2]
                change_favorite_list(recipe_id, new_list_id)

        data = {'list': current_list,
                'recipes': get_favorite_recipes(list_id)}

        return render_template('recipe/favorite-list.html',
                               segment=f'favorite-list-{list_id}',
                               user_id=current_user.id,
                               favorite_lists=get_favorite_lists(),
                               **data)
    else:
        return render_template('error/page-404.html'), 404
