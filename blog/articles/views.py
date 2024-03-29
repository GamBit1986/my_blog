from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.exceptions import NotFound
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload

from ..forms.articles import CreateArticleForm
from ..models import User, Article, Author, Tag
from ..extension import db

article = Blueprint(
    "article_problem", __name__, url_prefix="/article", static_folder="../static"
)


@article.route("/", methods=["GET"])
def article_list():
    articles: Article = Article.query.all()
    return render_template(
        "./articles/list.html",
        articles=articles,
    )


@article.route("/create", methods=["GET"])
@login_required
def create_article_form():
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    return render_template("articles/create.html", form=form)


@article.route("/", methods=["POST"])
@login_required
def create_article():
    form = CreateArticleForm(request.form)

    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]

    if form.validate_on_submit():
        _article = Article(title=form.title.data, text=form.text.data)

        
        if current_user.author:            
            _article.author_id = current_user.author.id
        else:
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            _article.author_id = author.id

        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                _article.tags.append(tag)

        db.session.add(_article)
        db.session.commit()        

        return redirect(url_for("article_problem.article_detail", article_id=_article.id))
    return render_template("articles/create.html", form=form)


@article.route("/<int:article_id>/")
@login_required
def article_detail(article_id: int):
    _article: Article = (
        Article.query.filter_by(id=article_id)
        .options(joinedload(Article.tags))
        .one_or_none()
    )
    if _article is None:
        raise NotFound
    return render_template("./articles/details.html", article=_article)
