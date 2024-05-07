# AI Recipes

> A webapp for discovering a wide range of recipes.

## Table of Contents

* [Introduction](#introduction)
* [Features](#features)
* [Screenshots](#screenshots)
* [Dependencies](#dependencies)
* [Setup](#setup)
* [Usage](#usage)
* [Acknowledgements](#acknowledgements)

## Introduction

- This app forms a versatile recipe book that is available from everywhere.
- On the base a dataset with over 20 million recipes is used.
- Additional data can be added to the existing database.

## Features

- Daily recommendations of unseen recipes
- Filter for recipes with matching ingredients
- Organizing of favorite recipes in collections

## Screenshots

TODO

## Dependencies

- [Dataset](https://huggingface.co/datasets/recipe_nlg)
- [Frontend](https://appseed.us/product/volt-dashboard/flask)
-
- [Flask](https://flask.palletsprojects.com)
- [WTForms](https://wtforms.readthedocs.io)
- pandas
- sqlalchemy

## Setup

Use `pip install -r requirements.txt` to install all necessary dependencies.
There are two requirement files, one for the data part (`./`) and one for the frontend (`./frontend`).

## Usage

- Use `python ./data_utils.py` to prepare the dataset and import it to the database.
- Use `python ./frontend/run.py` to start the webapp.
- Access the webinterface via `http://localhost:5000` or `http://127.0.0.1:5000`.
- Follow along the screenshots.

## To-Do

- Connect APIs of more recipe sources
- Option to add custom recipes
- Option to add notes to recipes

## Acknowledgements

This project was inspired by myself, since there was no alternative.

*Original idea in April 2024*
